import React, { useState, useEffect } from 'react';
import { Network, ZoomIn, ZoomOut, Maximize2, RefreshCw, ShieldAlert, Layers } from 'lucide-react';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import { graphApi, BusinessGraphData } from '@/api/graphApi';
import { BusinessGraphNode } from '@/types';

export const BusinessGraphPage: React.FC<{ onNavigate: (path: string) => void }> = ({
  onNavigate,
}) => {
  const [graphData, setGraphData] = useState<BusinessGraphData | null>(null);
  const [selectedNode, setSelectedNode] = useState<BusinessGraphNode | null>(null);
  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null);
  const [zoomLevel, setZoomLevel] = useState(1);

  useEffect(() => {
    graphApi.getBusinessGraph().then((data) => {
      setGraphData(data);
      setSelectedNode(data.nodes[0]);
    });
  }, []);

  if (!graphData) return null;

  // Pre-calculated layout positions for enterprise node graph
  const nodePositions: Record<string, { x: number; y: number }> = {
    fuel_energy: { x: 120, y: 140 },
    operating_costs: { x: 380, y: 150 },
    fleet_ops: { x: 220, y: 280 },
    driver_capacity: { x: 100, y: 380 },
    deliveries: { x: 420, y: 320 },
    warehousing: { x: 260, y: 80 },
    marketing_sales: { x: 580, y: 80 },
    client_retention: { x: 620, y: 240 },
    revenue: { x: 640, y: 380 },
    gross_margin: { x: 500, y: 200 },
    cash_flow: { x: 740, y: 180 },
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#FF6A00]/14 pb-5">
        <div>
          <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-wider">
            ENTERPRISE TOPOLOGICAL TWIN
          </span>
          <h1 className="text-2xl font-bold text-[#F5F0EA]">Business Dependency Graph</h1>
          <p className="text-xs font-mono text-[#A89D92] mt-0.5">
            NetworkX directed dependency topology • Interactive causal propagation & risk stress paths
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center bg-[#120C08] border border-[#FF6A00]/20 rounded-xl p-1 text-xs">
            <button
              onClick={() => setZoomLevel((z) => Math.max(0.7, z - 0.1))}
              className="p-1.5 text-[#A89D92] hover:text-[#F5F0EA]"
            >
              <ZoomOut className="w-4 h-4" />
            </button>
            <span className="px-2 font-mono text-xs text-[#FF8A24]">
              {Math.round(zoomLevel * 100)}%
            </span>
            <button
              onClick={() => setZoomLevel((z) => Math.min(1.4, z + 0.1))}
              className="p-1.5 text-[#A89D92] hover:text-[#F5F0EA]"
            >
              <ZoomIn className="w-4 h-4" />
            </button>
          </div>

          <GlowButton
            variant="secondary"
            size="sm"
            onClick={() => onNavigate('/investigation')}
          >
            Investigate Active Signal
          </GlowButton>
        </div>
      </div>

      {/* Main Interactive Canvas & Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Full-screen SVG Graph Environment */}
        <div className="lg:col-span-8 relative h-[560px] rounded-3xl bg-[#080604] border border-[#FF6A00]/25 overflow-hidden shadow-[0_0_40px_rgba(0,0,0,0.8)]">
          <div className="absolute inset-0 grid-pattern opacity-20 pointer-events-none" />

          {/* SVG Dependency Render */}
          <svg
            className="w-full h-full cursor-grab active:cursor-grabbing transition-transform duration-200"
            viewBox="0 0 860 480"
            style={{ transform: `scale(${zoomLevel})` }}
          >
            <defs>
              <linearGradient id="edgeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#FF6A00" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#FFB15A" stopOpacity="0.8" />
              </linearGradient>
              <linearGradient id="stressedGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#FF4500" stopOpacity="0.9" />
                <stop offset="100%" stopColor="#FF6A00" stopOpacity="0.9" />
              </linearGradient>
              <filter id="glow">
                <feGaussianBlur stdDeviation="3" result="coloredBlur" />
                <feMerge>
                  <feMergeNode in="coloredBlur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>

            {/* Render Connecting Directed Edges */}
            {graphData.edges.map((edge, idx) => {
              const p1 = nodePositions[edge.source];
              const p2 = nodePositions[edge.target];
              if (!p1 || !p2) return null;

              const isHighlighted =
                hoveredNodeId === edge.source || hoveredNodeId === edge.target;

              return (
                <g key={idx}>
                  <line
                    x1={p1.x}
                    y1={p1.y}
                    x2={p2.x}
                    y2={p2.y}
                    stroke={
                      edge.isStressed
                        ? 'url(#stressedGrad)'
                        : isHighlighted
                        ? '#FFB15A'
                        : 'rgba(255, 106, 0, 0.22)'
                    }
                    strokeWidth={edge.isStressed || isHighlighted ? 2.5 : 1.2}
                    strokeDasharray={edge.isStressed ? '4 4' : undefined}
                    filter={edge.isStressed ? 'url(#glow)' : undefined}
                  />
                </g>
              );
            })}

            {/* Render Graph Nodes */}
            {graphData.nodes.map((node) => {
              const pos = nodePositions[node.id] || { x: 300, y: 200 };
              const isSelected = selectedNode?.id === node.id;
              const isHovered = hoveredNodeId === node.id;

              return (
                <g
                  key={node.id}
                  transform={`translate(${pos.x}, ${pos.y})`}
                  onClick={() => setSelectedNode(node)}
                  onMouseEnter={() => setHoveredNodeId(node.id)}
                  onMouseLeave={() => setHoveredNodeId(null)}
                  className="cursor-pointer transition-all"
                >
                  {/* Outer Glow Halo if Stressed or Selected */}
                  {(node.status === 'critical' || isSelected) && (
                    <circle
                      r={24}
                      fill={node.status === 'critical' ? 'rgba(255,69,0,0.2)' : 'rgba(255,106,0,0.2)'}
                      className="animate-pulse"
                    />
                  )}

                  {/* Node Base Circle */}
                  <circle
                    r={16}
                    fill="#120C08"
                    stroke={
                      node.status === 'critical'
                        ? '#FF4500'
                        : node.status === 'warning'
                        ? '#FF8A24'
                        : '#FF6A00'
                    }
                    strokeWidth={isSelected ? 3 : 1.8}
                    filter={isSelected ? 'url(#glow)' : undefined}
                  />

                  {/* Inner Status Core */}
                  <circle
                    r={5}
                    fill={
                      node.status === 'critical'
                        ? '#FF4500'
                        : node.status === 'warning'
                        ? '#FFB15A'
                        : '#FF6A00'
                    }
                  />

                  {/* Node Label Text */}
                  <text
                    y={32}
                    textAnchor="middle"
                    fill="#F5F0EA"
                    fontSize={11}
                    fontFamily="Inter, sans-serif"
                    fontWeight={isSelected ? 'bold' : 'normal'}
                  >
                    {node.label}
                  </text>
                  <text
                    y={44}
                    textAnchor="middle"
                    fill="#A89D92"
                    fontSize={9}
                    fontFamily="monospace"
                  >
                    {node.value}
                  </text>
                </g>
              );
            })}
          </svg>
        </div>

        {/* Right: Selected Node Inspection Inspector */}
        <GlowCard className="lg:col-span-4 space-y-5">
          {selectedNode ? (
            <div>
              <div className="flex items-center justify-between">
                <span
                  className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono uppercase font-bold border ${
                    selectedNode.status === 'critical'
                      ? 'bg-[#FF4500]/20 text-[#FF4500] border-[#FF4500]/40'
                      : 'bg-[#FF6A00]/15 text-[#FFB15A] border-[#FF6A00]/30'
                  }`}
                >
                  {selectedNode.status.toUpperCase()} STATUS
                </span>
                <span className="text-xs font-mono text-[#A89D92]">Risk: {selectedNode.riskScore}/100</span>
              </div>

              <h3 className="text-xl font-bold text-[#F5F0EA] mt-3">{selectedNode.label}</h3>
              <p className="text-xs font-mono text-[#FF8A24] mt-1">Domain: {selectedNode.category.toUpperCase()}</p>

              <div className="mt-4 p-3 rounded-xl bg-[#080604] border border-[#FF6A00]/15 space-y-2 text-xs font-mono">
                <div className="flex justify-between">
                  <span className="text-[#6F665F]">Telemetry Value:</span>
                  <span className="text-[#F5F0EA] font-bold">{selectedNode.value}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[#6F665F]">Downstream Impact:</span>
                  <span className="text-[#FFB15A] font-bold">{selectedNode.dependencies.length} Connected Nodes</span>
                </div>
              </div>

              <div className="mt-5 space-y-2">
                <span className="text-[10px] font-mono uppercase text-[#A89D92] font-semibold block">
                  PROPAGATION DEPENDENCIES:
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {selectedNode.dependencies.map((dep) => (
                    <span
                      key={dep}
                      className="px-2.5 py-1 rounded-md bg-[#17100B] border border-[#FF6A00]/20 text-xs font-mono text-[#FFB15A]"
                    >
                      {dep}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <p className="text-xs font-mono text-[#6F665F]">Select a node in the graph to inspect</p>
          )}

          <div className="pt-4 border-t border-[#FF6A00]/12">
            <GlowButton
              size="sm"
              className="w-full"
              onClick={() => onNavigate('/simulation')}
            >
              Simulate Stress Shocks
            </GlowButton>
          </div>
        </GlowCard>
      </div>
    </div>
  );
};

export default BusinessGraphPage;
