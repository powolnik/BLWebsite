/**
 * BLACK LIGHT Collective — Scene Object 3D
 * R3F component that renders a single scene object as a translucent
 * bounding box with a wireframe overlay. Supports mouse drag to reposition.
 * Colour changes based on selection, hover, and collision state.
 */

import { useRef, useState, useEffect, useCallback } from 'react';
import { useThree } from '@react-three/fiber';
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
 * Supports drag-to-move on the horizontal plane.
 */
export default function SceneObject3D({ objectData }: Props) {
  const meshRef = useRef<THREE.Mesh>(null);
  const { selectedObjectId, collisions, showCollisions, selectObject, setHoveredObject, availableModels, moveSceneObject, setDragging, dragObjectId } = useSceneBuilderStore();
  const [hovered, setHovered] = useState(false);
  const { camera, gl } = useThree();
  const dragRef = useRef({ active: false, startMouse: new THREE.Vector2(), startPos: new THREE.Vector3() });
  const planeRef = useRef(new THREE.Plane(new THREE.Vector3(0, 1, 0), 0));
  const raycaster = useRef(new THREE.Raycaster());
  const intersectPoint = useRef(new THREE.Vector3());

  const isSelected = selectedObjectId === objectData.id;
  const isColliding = showCollisions && collisions.has(objectData.id);

  // Look up model metadata for labels (name, category, etc.)

  // Convert engine cm → Three.js metres
  const pos: [number, number, number] = [
    objectData.position.x / 100,
    objectData.position.y / 100,
    objectData.position.z / 100
  ];

  // Scaled bounding box size in metres
  const sizeArr: [number, number, number] = [
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

  const handlePointerDown = useCallback((e: any) => {
    e.stopPropagation();
    selectObject(objectData.id);

    // Start drag
    dragRef.current.active = true;
    dragRef.current.startPos.set(objectData.position.x, objectData.position.y, objectData.position.z);

    // Set drag plane at object's Y height (in world units = cm/100)
    planeRef.current.set(new THREE.Vector3(0, 1, 0), -objectData.position.y / 100);

    // Record mouse position in NDC
    const rect = gl.domElement.getBoundingClientRect();
    dragRef.current.startMouse.set(
      ((e.clientX - rect.left) / rect.width) * 2 - 1,
      -((e.clientY - rect.top) / rect.height) * 2 + 1
    );

    setDragging(true, objectData.id);
    gl.domElement.style.cursor = 'grabbing';
  }, [objectData.id, objectData.position, selectObject, setDragging, gl]);

  useEffect(() => {
    const handlePointerMove = (e: PointerEvent) => {
      if (!dragRef.current.active || dragObjectId !== objectData.id) return;

      const rect = gl.domElement.getBoundingClientRect();
      const mouse = new THREE.Vector2(
        ((e.clientX - rect.left) / rect.width) * 2 - 1,
        -((e.clientY - rect.top) / rect.height) * 2 + 1
      );

      raycaster.current.setFromCamera(mouse, camera);
      if (raycaster.current.ray.intersectPlane(planeRef.current, intersectPoint.current)) {
        // Convert back to cm
        const newX = intersectPoint.current.x * 100;
        const newZ = intersectPoint.current.z * 100;
        moveSceneObject(objectData.id, newX, objectData.position.y, newZ);
      }
    };

    const handlePointerUp = () => {
      if (dragRef.current.active) {
        dragRef.current.active = false;
        setDragging(false, null);
        gl.domElement.style.cursor = 'auto';
      }
    };

    gl.domElement.addEventListener('pointermove', handlePointerMove);
    gl.domElement.addEventListener('pointerup', handlePointerUp);
    return () => {
      gl.domElement.removeEventListener('pointermove', handlePointerMove);
      gl.domElement.removeEventListener('pointerup', handlePointerUp);
    };
  }, [objectData.id, objectData.position.y, camera, gl, moveSceneObject, setDragging, dragObjectId]);

  return (
    <group position={pos} rotation={rot}>
      {/* Solid translucent mesh — handles click, drag, and hover events */}
      <mesh
        ref={meshRef}
        onPointerDown={handlePointerDown}
        onPointerOver={(e: any) => { e.stopPropagation(); setHovered(true); setHoveredObject(objectData.id); gl.domElement.style.cursor = 'grab'; }}
        onPointerOut={() => { setHovered(false); setHoveredObject(null); if (!dragRef.current.active) gl.domElement.style.cursor = 'auto'; }}
      >
        <boxGeometry args={sizeArr} />
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
        <boxGeometry args={sizeArr} />
        <meshBasicMaterial color={color} wireframe transparent opacity={0.8} />
      </mesh>
    </group>
  );
}
