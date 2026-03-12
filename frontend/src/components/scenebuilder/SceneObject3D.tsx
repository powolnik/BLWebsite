/**
 * BLACK LIGHT Collective — Scene Object 3D
 * R3F component that renders a single scene object as a translucent
 * bounding box with a wireframe overlay. Supports click-to-select
 * and mouse drag to reposition on the horizontal plane.
 */

import { useRef, useState, useEffect, useCallback } from 'react';
import { useThree } from '@react-three/fiber';
import { useSceneBuilderStore } from '../../stores/sceneBuilderStore';
import type { SceneObjectData } from '../../engine/types';
import * as THREE from 'three';

interface Props {
  objectData: SceneObjectData;
}

/** No-op raycast function — makes a mesh invisible to pointer events */
const noRaycast = () => null;

export default function SceneObject3D({ objectData }: Props) {
  const meshRef = useRef<THREE.Mesh>(null);
  const {
    selectedObjectId, collisions, showCollisions,
    selectObject, setHoveredObject, moveSceneObject,
    setDragging, dragObjectId
  } = useSceneBuilderStore();

  const [hovered, setHovered] = useState(false);
  const { camera, gl } = useThree();

  // Drag state refs
  const dragRef = useRef({ active: false, startPos: new THREE.Vector3() });
  const planeRef = useRef(new THREE.Plane(new THREE.Vector3(0, 1, 0), 0));
  const raycaster = useRef(new THREE.Raycaster());
  const intersectPoint = useRef(new THREE.Vector3());

  const isSelected = selectedObjectId === objectData.id;
  const isColliding = showCollisions && collisions.has(objectData.id);

  // Convert engine cm → Three.js metres
  const pos: [number, number, number] = [
    objectData.position.x / 100,
    objectData.position.y / 100,
    objectData.position.z / 100
  ];

  const sizeArr: [number, number, number] = [
    (objectData.bboxSize.x * objectData.scale.x) / 100,
    (objectData.bboxSize.y * objectData.scale.y) / 100,
    (objectData.bboxSize.z * objectData.scale.z) / 100
  ];

  const rot: [number, number, number] = [
    THREE.MathUtils.degToRad(objectData.rotation.x),
    THREE.MathUtils.degToRad(objectData.rotation.y),
    THREE.MathUtils.degToRad(objectData.rotation.z)
  ];

  // Colour based on state: collision > selected > hovered > default
  let color = '#00d4ff';
  if (isColliding) color = '#ff2244';
  if (isSelected) color = '#ffaa00';
  if (hovered && !isSelected) color = '#44ffaa';

  /** Pointer down — select + start drag */
  const handlePointerDown = useCallback((e: any) => {
    e.stopPropagation();
    selectObject(objectData.id);

    dragRef.current.active = true;
    dragRef.current.startPos.set(
      objectData.position.x, objectData.position.y, objectData.position.z
    );

    // Drag plane at object's Y height (world units = metres)
    planeRef.current.set(
      new THREE.Vector3(0, 1, 0),
      -objectData.position.y / 100
    );

    setDragging(true, objectData.id);
    gl.domElement.style.cursor = 'grabbing';
  }, [objectData.id, objectData.position, selectObject, setDragging, gl]);

  /** Pointer over — hover highlight */
  const handlePointerOver = useCallback((e: any) => {
    e.stopPropagation();
    setHovered(true);
    setHoveredObject(objectData.id);
    if (!dragRef.current.active) gl.domElement.style.cursor = 'grab';
  }, [objectData.id, setHoveredObject, gl]);

  /** Pointer out — remove hover */
  const handlePointerOut = useCallback(() => {
    setHovered(false);
    setHoveredObject(null);
    if (!dragRef.current.active) gl.domElement.style.cursor = 'auto';
  }, [setHoveredObject, gl]);

  // Global pointer move/up for drag
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
      {/* Solid translucent mesh — handles all pointer events */}
      <mesh
        ref={meshRef}
        onPointerDown={handlePointerDown}
        onPointerOver={handlePointerOver}
        onPointerOut={handlePointerOut}
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

      {/* Wireframe overlay — MUST NOT intercept raycasts */}
      <mesh raycast={noRaycast}>
        <boxGeometry args={sizeArr} />
        <meshBasicMaterial color={color} wireframe transparent opacity={0.8} />
      </mesh>

      {/* Selection indicator ring */}
      {isSelected && (
        <mesh position={[0, -sizeArr[1] / 2 + 0.01, 0]} rotation={[-Math.PI / 2, 0, 0]} raycast={noRaycast}>
          <ringGeometry args={[
            Math.max(sizeArr[0], sizeArr[2]) * 0.6,
            Math.max(sizeArr[0], sizeArr[2]) * 0.65,
            32
          ]} />
          <meshBasicMaterial color="#ffaa00" transparent opacity={0.6} />
        </mesh>
      )}
    </group>
  );
}
