/**
 * BLACK LIGHT Collective — Scene Object 3D
 * R3F component that renders a single scene object as a translucent
 * bounding box with a wireframe overlay. Colour changes based on
 * selection, hover, and collision state.
 */

import { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { useSceneBuilderStore } from '../../stores/sceneBuilderStore';
import type { SceneObjectData } from '../../engine/types';
import * as THREE from 'three';

/** Props for SceneObject3D */
interface Props {
  objectData: SceneObjectData;
}

/**
 * SceneObject3D — renders a single object in the 3D scene.
 * Uses a coloured box for the solid body and a wireframe overlay for edges.
 * Colour logic: cyan (default) → red (colliding) → orange (selected) → green (hovered).
 */
export default function SceneObject3D({ objectData }: Props) {
  const meshRef = useRef<THREE.Mesh>(null);
  const { selectedObjectId, collisions, showCollisions, selectObject, setHoveredObject, availableModels } = useSceneBuilderStore();
  const [hovered, setHovered] = useState(false);

  const isSelected = selectedObjectId === objectData.id;
  const isColliding = showCollisions && collisions.has(objectData.id);

  // Look up model metadata for labels (name, category, etc.)
  const model = availableModels.find(m => m.id === objectData.modelId);

  // Convert engine cm → Three.js metres
  const pos: [number, number, number] = [
    objectData.position.x / 100,
    objectData.position.y / 100,
    objectData.position.z / 100
  ];

  // Scaled bounding box size in metres
  const size: [number, number, number] = [
    (objectData.bboxSize.x * objectData.scale.x) / 100,
    (objectData.bboxSize.y * objectData.scale.y) / 100,
    (objectData.bboxSize.z * objectData.scale.z) / 100
  ];

  // Convert Euler degrees → radians using THREE.MathUtils
  const rot: [number, number, number] = [
    THREE.MathUtils.degToRad(objectData.rotation.x),
    THREE.MathUtils.degToRad(objectData.rotation.y),
    THREE.MathUtils.degToRad(objectData.rotation.z)
  ];

  // Determine colour based on object state (priority: collision > selected > hovered > default)
  let color = '#00d4ff'; // default cyan
  if (isColliding) color = '#ff2244';
  if (isSelected) color = '#ffaa00';
  if (hovered && !isSelected) color = '#44ffaa';

  // Per-frame update hook (placeholder for future animations)
  useFrame((_, delta) => {
    if (meshRef.current && isSelected) {
      meshRef.current.rotation.y += delta * 0.0; // no auto-rotate, reserved for future use
    }
  });

  return (
    <group position={pos} rotation={rot}>
      {/* Solid translucent mesh — handles click and hover events */}
      <mesh
        ref={meshRef}
        onClick={(e: any) => { e.stopPropagation(); selectObject(objectData.id); }}
        onPointerOver={(e: any) => { e.stopPropagation(); setHovered(true); setHoveredObject(objectData.id); }}
        onPointerOut={() => { setHovered(false); setHoveredObject(null); }}
      >
        <boxGeometry args={size} />
        <meshStandardMaterial
          color={color}
          transparent
          opacity={isSelected ? 0.7 : 0.5}
          emissive={color}
          emissiveIntensity={isSelected ? 0.3 : 0.1}
        />
      </mesh>

      {/* Wireframe overlay for edge visibility */}
      <mesh>
        <boxGeometry args={size} />
        <meshBasicMaterial color={color} wireframe transparent opacity={0.8} />
      </mesh>

      {/* Label placeholder — would use <Html> from drei for floating labels */}
      {isSelected && model && (
        <group position={[0, size[1] / 2 + 0.3, 0]}>
          {/* Reserved for future Html overlay label */}
        </group>
      )}
    </group>
  );
}
