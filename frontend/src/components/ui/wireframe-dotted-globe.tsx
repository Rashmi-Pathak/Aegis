import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import * as topojson from 'topojson-client';
import landData from '@/assets/land-110m.json';
import { Maximize2, Sun, RotateCcw } from 'lucide-react';

interface RotatingEarthProps {
  width?: number;
  height?: number;
  className?: string;
}

export const RotatingEarth: React.FC<RotatingEarthProps> = ({
  width = 640,
  height = 640,
  className = '',
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);

  const [scaleFactor, setScaleFactor] = useState(1);
  const [isRotating, setIsRotating] = useState(true);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    ctx.scale(dpr, dpr);

    // Extract GeoJSON land feature from TopoJSON
    const land: any = topojson.feature(landData as any, (landData as any).objects.land);

    // Generate accurate continent dots based on real geography
    const landDots: [number, number][] = [];
    for (let lat = -75; lat <= 80; lat += 2.8) {
      const step = Math.max(2.8, 2.8 / Math.cos((lat * Math.PI) / 180));
      for (let lon = -180; lon < 180; lon += step) {
        if (d3.geoContains(land, [lon, lat])) {
          landDots.push([lon, lat]);
        }
      }
    }

    const baseRadius = Math.min(width, height) / 2 - 35;
    let currentScale = baseRadius * scaleFactor;

    const projection = d3
      .geoOrthographic()
      .scale(currentScale)
      .translate([width / 2, height / 2])
      .clipAngle(90);

    const path = d3.geoPath(projection, ctx);
    const graticule = d3.geoGraticule().step([15, 15])();

    let rotation: [number, number, number] = [-20, -15, 0];
    let isDragging = false;
    let startPos = { x: 0, y: 0 };
    let animationFrameId: number;

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      currentScale = baseRadius * scaleFactor;
      projection.scale(currentScale);

      // 1. Globe Outer Border Circle
      ctx.beginPath();
      ctx.arc(width / 2, height / 2, currentScale, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.45)';
      ctx.lineWidth = 1;
      ctx.stroke();

      // Background fill of globe
      ctx.fillStyle = '#000000';
      ctx.fill();

      // 2. Graticule Wireframe Lines (meridians and parallels)
      ctx.beginPath();
      path(graticule);
      ctx.lineWidth = 0.45;
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.18)';
      ctx.stroke();

      // 3. Continental Coastline Outlines
      ctx.beginPath();
      path(land);
      ctx.lineWidth = 0.85;
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.65)';
      ctx.stroke();

      // 4. Dotted Matrix filling Landmasses
      const centerLon = -rotation[0];
      const centerLat = -rotation[1];

      for (let i = 0; i < landDots.length; i++) {
        const pt = landDots[i];
        const dist = d3.geoDistance(pt, [centerLon, centerLat]);

        if (dist < Math.PI / 2) {
          const coords = projection(pt);
          if (coords) {
            const alpha = Math.max(0.2, Math.cos(dist));
            ctx.beginPath();
            ctx.arc(coords[0], coords[1], 0.95, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${alpha * 0.95})`;
            ctx.fill();
          }
        }
      }

      // Continuous automatic rotation
      if (isRotating && !isDragging) {
        rotation[0] += 0.35;
        projection.rotate(rotation);
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    // Mouse drag interaction
    const onMouseDown = (e: MouseEvent) => {
      isDragging = true;
      startPos = { x: e.clientX, y: e.clientY };
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      const dx = e.clientX - startPos.x;
      const dy = e.clientY - startPos.y;

      rotation[0] += dx * 0.35;
      rotation[1] -= dy * 0.35;
      rotation[1] = Math.max(-80, Math.min(80, rotation[1]));
      projection.rotate(rotation);

      startPos = { x: e.clientX, y: e.clientY };
    };

    const onMouseUp = () => {
      isDragging = false;
    };

    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      setScaleFactor((prev) => Math.max(0.65, Math.min(1.8, prev - e.deltaY * 0.0012)));
    };

    canvas.addEventListener('mousedown', onMouseDown);
    canvas.addEventListener('wheel', onWheel, { passive: false });
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);

    return () => {
      cancelAnimationFrame(animationFrameId);
      canvas.removeEventListener('mousedown', onMouseDown);
      canvas.removeEventListener('wheel', onWheel);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
    };
  }, [width, height, scaleFactor, isRotating]);

  return (
    <div
      ref={containerRef}
      className={`relative flex items-center justify-center select-none bg-black rounded-lg overflow-hidden border border-white/10 ${className}`}
      style={{ width: `${width}px`, height: `${height}px` }}
    >
      {/* Top Left Controls: Fullscreen, Sun/Moon, Reset/Pause */}
      <div className="absolute top-4 left-4 z-20 flex items-center gap-2">
        <button
          onClick={() => {
            if (containerRef.current) {
              if (document.fullscreenElement) {
                document.exitFullscreen();
              } else {
                containerRef.current.requestFullscreen();
              }
            }
          }}
          className="p-2 rounded-lg bg-white/5 hover:bg-white/15 border border-white/15 text-white/70 hover:text-white transition-all text-xs"
          title="Toggle Fullscreen"
        >
          <Maximize2 className="w-3.5 h-3.5" />
        </button>
        <button
          onClick={() => {}}
          className="p-2 rounded-lg bg-white/5 hover:bg-white/15 border border-white/15 text-white/70 hover:text-white transition-all text-xs"
          title="Light/Dark Mode"
        >
          <Sun className="w-3.5 h-3.5" />
        </button>
        <button
          onClick={() => setIsRotating((prev) => !prev)}
          className={`p-2 rounded-lg border text-xs transition-all ${
            isRotating
              ? 'bg-white/15 border-white/30 text-white'
              : 'bg-white/5 border-white/15 text-white/60'
          }`}
          title="Toggle Rotation"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Main D3 Canvas */}
      <canvas
        ref={canvasRef}
        style={{ width: `${width}px`, height: `${height}px` }}
        className="cursor-grab active:cursor-grabbing"
      />

      {/* Bottom Left Badge exactly as in 21st.dev reference */}
      <div className="absolute bottom-4 left-4 z-20 px-3 py-1.5 rounded-md bg-white/5 backdrop-blur-md border border-white/10 text-[11px] font-mono text-white/60 tracking-wider">
        Drag to rotate • Scroll to zoom
      </div>
    </div>
  );
};

export default RotatingEarth;
