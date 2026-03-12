/**
 * BLACK LIGHT Collective — Scene Builder 3D Canvas
 * React Three Fiber canvas that renders the 3D scene.
 * Contains the ground plane, grid, scene objects, physics indicators,
 * and orbit camera controls. OrbitControls are disabled during drag.
 */

import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';
import { useSceneBuilderStore } from '../../stores/sceneBuilderStore';
import CubicGrid from './CubicGrid';
import SceneObject3D from './SceneObject3D';
import { useCallback } from 'react';
import * as THREE from 'three';

/**
 * Inner scene content rendered inside the R3F Canvas.
 * Must be a child of <Canvas> to access the Three.js context.
 */
function SceneContent() {
  const sceneObjects = useSceneBuilderStore(s => s.sceneObjects);
  const selectObject = useSceneBuilderStore(s => s.selectObject);
  const engine = useSceneBuilderStore(s => s.engine);
  const showPhysics = useSceneBuilderStore(s => s.showPhysics);
  const physics = useSceneBuilderStore(s => s.physics);
  const isDragging = useSceneBuilderStore(s => s.isDragging);

  /** Clicking the ground plane deselects any selected object */
  const handleGroundClick = useCallback(() => {
    selectObject(null);
  }, [selectObject]);

  // Convert cm → metres for Three.js scene units
  const gridW = engine.getGridWidth() / 100;
  const gridD = engine.getGridDepth() / 100;

  return (
    <>
      {/* Scene lighting */}
      <ambientLight intensity={0.4} />
      <directionalLight position={[10, 20, 10]} intensity={0.8} castShadow />
      <directionalLight position={[-10, 15, -10]} intensity={0.3} />
      {/* drei Environment preset for realistic reflections */}
      <Environment preset="night" />

      {/* Cubic grid boundary and axis indicators */}
      <CubicGrid />

      {/* Invisible ground plane for click-to-deselect */}
      <mesh
        position={[gridW / 2, -0.01, gridD / 2]}
        rotation={[-Math.PI / 2, 0, 0]}
        onClick={handleGroundClick}
        receiveShadow
      >
        <planeGeometry args={[gridW, gridD]} />
        <meshStandardMaterial color="#0a0a14" transparent opacity={0.8} />
      </mesh>

      {/* Render each scene object as a 3D bounding box */}
      {Array.from(sceneObjects.values()).map(obj => (
        <SceneObject3D key={obj.id} objectData={obj} />
      ))}

      {/* Centre-of-mass indicator sphere (green = stable, red = unstable) */}
      {showPhysics && physics.totalWeight > 0 && (
        <mesh position={[
          physics.centerOfMass.x / 100,
          physics.centerOfMass.y / 100,
          physics.centerOfMass.z / 100
        ]}>
          <sphereGeometry args={[0.15, 16, 16]} />
          <meshStandardMaterial
            color={physics.isStable ? '#00ff88' : '#ff4444'}
            emissive={physics.isStable ? '#00ff88' : '#ff4444'}
            emissiveIntensity={0.5}
          />
        </mesh>
      )}

      {/* Orbit camera controls with constrained zoom — disabled during drag */}
      <OrbitControls
        makeDefault
        enabled={!isDragging}
        minDistance={2}
        maxDistance={50}
        target={[gridW / 2, 0, gridD / 2]}
      />
    </>
  );
}

/**
 * SceneCanvas — top-level wrapper that creates the R3F Canvas.
 * Configures shadows, camera, tone mapping (ACES Filmic), and clear colour.
 */
export default function SceneCanvas() {
  return (
    <div className="w-full h-full bg-[#0a0a14]">
      <Canvas
        shadows
        camera={{
          position: [15, 12, 15],
          fov: 50,
          near: 0.1,
          far: 1000
        }}
        gl={{ antialias: true, alpha: false }}
        onCreated={({ gl }) => {
          gl.setClearColor('#0a0a14');
          // ACES Filmic tone mapping for cinematic look
          gl.toneMapping = THREE.ACESFilmicToneMapping;
          gl.toneMappingExposure = 1.2;
        }}
      >
        <SceneContent />
      </Canvas>
    </div>
  );
}
