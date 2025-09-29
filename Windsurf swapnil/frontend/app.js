let renderer, scene, camera, controls;
const viewerEl = document.getElementById('viewer');
const statusEl = document.getElementById('status');
const resultEl = document.getElementById('result');
const meshLinkEl = document.getElementById('mesh-link');

init3D();
setupForm();
window.addEventListener('resize', onResize);

function init3D() {
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0b1020);

  const w = viewerEl.clientWidth;
  const h = viewerEl.clientHeight;
  camera = new THREE.PerspectiveCamera(60, w / h, 0.1, 1000);
  camera.position.set(3, 2, 4);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(w, h);
  viewerEl.innerHTML = '';
  viewerEl.appendChild(renderer.domElement);

  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  // Lighting
  const hemi = new THREE.HemisphereLight(0xffffff, 0x202040, 1.0);
  scene.add(hemi);
  const dir = new THREE.DirectionalLight(0xffffff, 1.2);
  dir.position.set(5, 10, 7);
  scene.add(dir);

  // Grid & axes (optional)
  const grid = new THREE.GridHelper(10, 10, 0x334155, 0x1e293b);
  grid.position.y = -1.01;
  scene.add(grid);

  animate();
}

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

function onResize() {
  const w = viewerEl.clientWidth;
  const h = viewerEl.clientHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
}

function setupForm() {
  const form = document.getElementById('gen-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    setStatus('Generating 3D model...');
    toggleForm(form, true);

    try {
      const fd = new FormData(form);
      const res = await fetch('/generate-3d', {
        method: 'POST',
        body: fd,
      });
      if (!res.ok) throw new Error('Request failed');
      const data = await res.json();

      if (data.status !== 'success' || !data.mesh_file) {
        throw new Error('Backend did not return a mesh_file');
      }

      const meshUrl = '/' + data.mesh_file.replace(/^\/+/, '');
      meshLinkEl.href = meshUrl;
      resultEl.classList.remove('hidden');
      setStatus('Loading mesh into viewer...');

      await loadOBJ(meshUrl);
      setStatus('Done');
    } catch (err) {
      console.error(err);
      setStatus('Error: ' + (err?.message || 'unknown'));
    } finally {
      toggleForm(form, false);
    }
  });
}

function toggleForm(form, disabled) {
  const btn = form.querySelector('button[type="submit"]');
  if (btn) btn.disabled = disabled;
}

function setStatus(text) {
  statusEl.textContent = text || '';
}

async function loadOBJ(url) {
  // Clear previous mesh
  for (let i = scene.children.length - 1; i >= 0; i--) {
    const obj = scene.children[i];
    if (obj.userData && obj.userData.isGeneratedMesh) {
      scene.remove(obj);
    }
  }

  const loader = new THREE.OBJLoader();
  return new Promise((resolve, reject) => {
    loader.load(
      url,
      (object) => {
        // Compute bounding box to center & scale
        const box = new THREE.Box3().setFromObject(object);
        const size = new THREE.Vector3();
        box.getSize(size);
        const center = new THREE.Vector3();
        box.getCenter(center);

        object.traverse((child) => {
          if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
          }
        });

        object.position.sub(center); // center at origin

        const maxDim = Math.max(size.x, size.y, size.z) || 1;
        const scale = 2 / maxDim; // fit roughly within [-1, 1]
        object.scale.setScalar(scale);

        object.userData.isGeneratedMesh = true;
        scene.add(object);
        controls.reset();
        camera.position.set(3, 2, 4);
        resolve();
      },
      undefined,
      (err) => reject(err)
    );
  });
}
