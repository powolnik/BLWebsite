/**
 * BLACK LIGHT Collective — Cubic Grid Overlay
 * Renders the 3D grid boundary, ground grid, axis lines, and height
 * markers inside the R3F scene. All engine values are in cm;
 * Three.js units are in metres (÷100).
 */

import { Grid, Line } from '@react-three/drei';
import { useSceneBuilderStore } from '../../stores/sceneBuilderStore';
import { useMemo } from 'react';

/**
 * CubicGrid — a visual representation of the scene's spatial boundaries.
 * Displays a floor grid, dashed boundary edges, height tick marks, and
 * coloured axis lines (X=red, Y=green, Z=blue).
 */
export default function CubicGrid() {
  const { engine, showGrid, gridCellDisplay } = useSceneBuilderStore();

  // Read engine dimensions (cm)
  const gridW = engine.getGridWidth();
  const gridH = engine.getGridHeight();
  const gridD = engine.getGridDepth();

  // Convert cm → metres for Three.js (1 unit = 1 metre)
  const w = gridW / 100; // 20 m
  const h = gridH / 100; // 10 m
  const d = gridD / 100; // 20 m
  const cellSize = gridCellDisplay / 100; // grid spacing in metres

  // Precompute the 8 dashed boundary edge lines + 4 top edges
  const edgeLines = useMemo(() => {
    const lines: [number, number, number][][] = [
      // 4 vertical edges
      [[0, 0, 0], [0, h, 0]],
      [[w, 0, 0], [w, h, 0]],
      [[0, 0, d], [0, h, d]],
      [[w, 0, d], [w, h, d]],
      // Top rectangle
      [[0, h, 0], [w, h, 0]],
      [[w, h, 0], [w, h, d]],
      [[w, h, d], [0, h, d]],
      [[0, h, d], [0, h, 0]],
    ];
    return lines;
  }, [w, h, d]);

  // Height markers — small tick lines on the Y axis at each grid interval
  const heightMarkers = useMemo(() => {
    const markers: [number, number, number][][] = [];
    for (let y = cellSize; y <= h; y += cellSize) {
      markers.push([[0, y, 0], [0.3, y, 0]]); // tick along X
      markers.push([[0, y, 0], [0, y, 0.3]]); // tick along Z
    }
    return markers;
  }, [h, cellSize]);

  // Early return when grid is toggled off
  if (!showGrid) return null;

  return (
    <group>
      {/* drei Grid helper on the ground plane */}
      <Grid
        position={[w / 2, 0.001, d / 2]}
        args={[w, d]}
        cellSize={cellSize}
        cellThickness={0.5}
        cellColor="#1a1a2e"
        sectionSize={cellSize * 5}
        sectionThickness={1}
        sectionColor="#16213e"
        fadeDistance={50}
        fadeStrength={1}
        infiniteGrid={false}
      />

      {/* Dashed boundary edges */}
      {edgeLines.map((points, i) => (
        <Line
          key={`edge-${i}`}
          points={points as any}
          color="#0f3460"
          lineWidth={1}
          dashed
          dashSize={0.2}
          gapSize={0.1}
        />
      ))}

      {/* Height markers (red ticks on the Y axis) */}
      {heightMarkers.map((points, i) => (
        <Line
          key={`hm-${i}`}
          points={points as any}
          color="#e94560"
          lineWidth={1}
        />
      ))}

      {/* Coloured axis lines extending slightly beyond the grid */}
      <Line points={[[0,0,0], [w + 1, 0, 0]]} color="#ff0000" lineWidth={2} /> {/* X axis */}
      <Line points={[[0,0,0], [0, h + 1, 0]]} color="#00ff00" lineWidth={2} /> {/* Y axis */}
      <Line points={[[0,0,0], [0, 0, d + 1]]} color="#0000ff" lineWidth={2} /> {/* Z axis */}
    </group>
  );
}
