import React, { useState, useEffect, useMemo, useRef } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';
import { Activity, Droplets, AlertTriangle, Play, RefreshCw, BarChart3, Map as MapIcon, Pause } from 'lucide-react';

const App = () => {
    const [allHistory, setAllHistory] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);
    const [graphData, setGraphData] = useState({ nodes: [], links: [] });
    const [loading, setLoading] = useState(true);
    const [playbackSpeed, setPlaybackSpeed] = useState(150);
    const [selectedArea, setSelectedArea] = useState('velachery'); // Default
    const [manifest, setManifest] = useState({ areas: [] });

    const fgRef = useRef();

    // Set up D3 forces for better separation
    useEffect(() => {
        if (fgRef.current) {
            fgRef.current.d3Force('charge').strength(-400);
            fgRef.current.d3Force('link').distance(80);
        }
    }, [loading]);

    // Load Manifest
    useEffect(() => {
        const fetchManifest = async () => {
            try {
                // Add timestamp to bypass cache
                const res = await fetch(`/data/manifest.json?t=${Date.now()}`);
                const data = await res.json();
                setManifest(data);
            } catch (err) {
                console.error("Error loading manifest:", err);
            }
        };
        fetchManifest();
    }, []);

    // Load Data for Selected Area
    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const timestamp = Date.now();
                const graphRes = await fetch(`/data/areas/${selectedArea}/graph.json?t=${timestamp}`);
                const graphJson = await graphRes.json();

                const historyRes = await fetch(`/results/areas/${selectedArea}/run_log.json?t=${timestamp}`);
                const historyJson = await historyRes.json();
                setAllHistory(historyJson);
                setCurrentIndex(0); // Reset on area change

                // Convert graph to force-graph format with geographic positioning
                const lons = graphJson.nodes.map(n => n.pos[0]);
                const lats = graphJson.nodes.map(n => n.pos[1]);
                const minLon = Math.min(...lons), maxLon = Math.max(...lons);
                const minLat = Math.min(...lats), maxLat = Math.max(...lats);

                // Better scaling for the viewport - Increase range to spread congested nodes
                const scaleX = (val) => (val - minLon) / (maxLon - minLon) * 2000 - 1000;
                const scaleY = (val) => (maxLat - val) / (maxLat - minLat) * 1600 - 800;

                const processedNodes = graphJson.nodes.map(n => ({
                    ...n,
                    x: scaleX(n.pos[0]), // Use x/y instead of fx/fy to allow force layout to adjust
                    y: scaleY(n.pos[1]),
                    color: n.type === 'outlet' ? '#3b82f6' : '#22c55e',
                    size: n.type === 'outlet' ? 10 : 6
                }));

                setGraphData({
                    nodes: processedNodes,
                    links: graphJson.links.map(l => ({
                        ...l,
                        color: '#1e293b'
                    }))
                });
                setLoading(false);
            } catch (err) {
                console.error("Error loading area data:", err);
                setLoading(false);
            }
        };
        fetchData();
    }, [selectedArea]);

    // Playback Logic
    useEffect(() => {
        let timer;
        if (isPlaying && currentIndex < allHistory.length - 1) {
            timer = setTimeout(() => {
                setCurrentIndex(prev => prev + 1);
            }, playbackSpeed);
        } else if (currentIndex >= allHistory.length - 1) {
            setIsPlaying(false);
        }
        return () => clearTimeout(timer);
    }, [isPlaying, currentIndex, allHistory, playbackSpeed]);

    // Derived State for Current Step
    const currentStats = useMemo(() => {
        return allHistory[currentIndex] || {
            flooded_nodes: 0,
            blocked_pipes: 0,
            total_flow: 0,
            cascade_depth: 0,
            resilience: 1.0
        };
    }, [allHistory, currentIndex]);

    // Update graph visual state based on current playback step
    const displayData = useMemo(() => {
        if (!graphData.nodes.length) return graphData;

        // Use specific identifiers if available, or simulate for viz
        const floodLimit = currentStats.flooded_nodes;
        const blockLimit = currentStats.blocked_pipes;

        return {
            nodes: graphData.nodes.map((n, i) => {
                const isFlooded = i < floodLimit;
                return {
                    ...n,
                    isFlooded,
                    color: isFlooded ? '#ef4444' : (n.type === 'outlet' ? '#3b82f6' : '#22c55e'),
                    val: isFlooded ? 14 : (n.type === 'outlet' ? 12 : 8)
                };
            }),
            links: graphData.links.map((l, i) => {
                const isBlocked = i < blockLimit;
                return {
                    ...l,
                    isBlocked,
                    color: isBlocked ? '#ef4444' : '#334155',
                    width: isBlocked ? 4 : 2,
                    particleSpeed: isBlocked ? 0 : 0.03
                };
            })
        };
    }, [graphData, currentStats]);

    const handleRun = () => {
        if (currentIndex >= allHistory.length - 1) setCurrentIndex(0);
        setIsPlaying(!isPlaying);
    };

    const handleReset = () => {
        setIsPlaying(false);
        setCurrentIndex(0);
    };

    if (loading) return <div className="min-h-screen bg-slate-950 flex items-center justify-center text-blue-400 font-bold">Initializing Simulation Engine...</div>;

    return (
        <div className="min-h-screen bg-slate-950 p-6 flex flex-col gap-6 font-sans text-slate-200">
            {/* Professional Header */}
            <header className="glass rounded-2xl p-6 flex justify-between items-center shadow-2xl border border-white/5 bg-slate-900/40 backdrop-blur-xl">
                <div className="flex items-center gap-6">
                    <div className="w-14 h-14 bg-gradient-to-br from-blue-600 to-blue-400 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-500/30">
                        <Activity className="text-white" size={32} />
                    </div>
                    <div>
                        <div className="flex items-center gap-2">
                            <h1 className="text-3xl font-black tracking-tighter text-white uppercase italic leading-none">
                                DrainFlex <span className="text-blue-500">PRO</span>
                            </h1>
                            <span className="bg-blue-500/10 text-blue-400 text-[10px] px-2 py-0.5 rounded-full border border-blue-500/20 font-bold uppercase tracking-widest">Enterprise</span>
                        </div>
                        <p className="text-slate-500 text-xs font-bold uppercase tracking-[0.2em] mt-1.5 flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                            Urban Flood Propagation Analysis • V2.5.0
                        </p>
                    </div>
                </div>

                <div className="flex items-center gap-6 bg-slate-950/50 p-3 rounded-2xl border border-white/5 ring-1 ring-white/5">
                    <div className="px-6 py-1 text-center border-r border-white/10">
                        <span className="block text-[10px] text-slate-500 font-bold uppercase tracking-widest mb-1">Time Elapsed</span>
                        <div className="flex items-baseline gap-1">
                            <span className="text-2xl font-mono font-black text-blue-400 leading-none">{currentIndex}</span>
                            <span className="text-[10px] font-bold text-slate-600">STEPS</span>
                        </div>
                    </div>
                    <div className="flex gap-3">
                        <button
                            onClick={handleRun}
                            className={`flex items-center gap-3 px-8 py-3 rounded-xl font-black transition-all shadow-xl active:scale-95 text-xs uppercase tracking-widest ${isPlaying ? 'bg-amber-500 hover:bg-amber-400 text-black shadow-amber-500/20' : 'bg-blue-600 hover:bg-blue-500 text-white shadow-blue-600/20'
                                }`}
                        >
                            {isPlaying ? <><Pause size={16} fill="black" /> Pause</> : <><Play size={16} fill="white" /> {currentIndex > 0 ? 'Resume' : 'Simulate'}</>}
                        </button>
                        <button
                            onClick={handleReset}
                            className="flex items-center gap-3 px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-black transition-all border border-slate-700 text-xs uppercase tracking-widest active:scale-95 shadow-lg"
                        >
                            <RefreshCw size={16} /> Reset
                        </button>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <div className="grid grid-cols-12 gap-6 flex-1 h-full min-h-0">

                {/* Graph Viewport */}
                <div className="col-span-8 glass rounded-[2.5rem] overflow-hidden relative border border-white/5 flex flex-col shadow-2xl bg-slate-950/40">
                    <div className="p-5 border-b border-white/5 flex justify-between items-center bg-slate-900/20">
                        <div className="flex items-center gap-3">
                            <div className="flex items-center gap-3 px-4 py-1.5 bg-slate-950/80 rounded-xl text-[10px] font-black tracking-widest border border-white/10 text-slate-300">
                                <MapIcon size={14} className="text-blue-400" />
                                STUDY AREA: {manifest.areas.find(a => a.id === selectedArea)?.label.toUpperCase() || 'LOADING...'}
                            </div>

                            <select
                                value={selectedArea}
                                onChange={(e) => setSelectedArea(e.target.value)}
                                className="bg-slate-900 border border-white/10 text-[10px] font-black uppercase tracking-widest px-3 py-1.5 rounded-xl text-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 cursor-pointer"
                            >
                                {manifest.areas.map(area => (
                                    <option key={area.id} value={area.id}>{area.label}</option>
                                ))}
                            </select>
                        </div>
                        <div className="flex gap-6 text-[10px] font-black text-slate-500 tracking-tighter">
                            <div className="flex items-center gap-2 px-3 py-1 bg-slate-950 rounded-lg"><div className="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.4)]"></div> JUNCTION</div>
                            <div className="flex items-center gap-2 px-3 py-1 bg-slate-950 rounded-lg"><div className="w-2.5 h-2.5 rounded-full bg-red-500 shadow-[0_0_12px_rgba(239,68,68,0.4)]"></div> FLOODED</div>
                            <div className="flex items-center gap-2 px-3 py-1 bg-slate-950 rounded-lg"><div className="w-2.5 h-2.5 rounded-full bg-blue-500 shadow-[0_0_12px_rgba(59,130,246,0.4)]"></div> OUTLET</div>
                        </div>
                    </div>
                    <div className="flex-1 min-h-0 relative">
                        <ForceGraph2D
                            ref={fgRef}
                            graphData={displayData}
                            d3AlphaDecay={0.02}
                            d3VelocityDecay={0.3}
                            warmupTicks={100}
                            cooldownTicks={100}
                            onEngineStop={() => fgRef.current.zoomToFit(400)}
                            nodeLabel={n => `[${n.type.toUpperCase()}] ID: ${n.id}\nElevation: ${n.elev?.toFixed(2)}m\nStatus: ${n.isFlooded ? 'CRITICAL' : 'OPERATIONAL'}`}
                            nodeColor={node => node.color}
                            linkColor={link => link.color}
                            linkWidth={link => link.width || 2}
                            linkDirectionalParticles={4}
                            linkDirectionalParticleWidth={2}
                            linkDirectionalParticleSpeed={link => link.particleSpeed || 0.03}
                            linkDirectionalArrowLength={4}
                            linkDirectionalArrowRelPos={1}
                            backgroundColor="#020617"
                            nodeCanvasObject={(node, ctx, globalScale) => {
                                // PROFESSIONAL NODE RENDERING
                                const label = node.id;

                                // Responsive base radius: switch from physical pixels to a better screen-relative size
                                const baseRadius = node.val / (globalScale * 0.5 + 0.5);
                                const radius = Math.max(baseRadius, 3 / globalScale);

                                // 1. OUTER GLOW/HALO
                                ctx.beginPath();
                                ctx.arc(node.x, node.y, radius + 4 / globalScale, 0, 2 * Math.PI, false);
                                ctx.fillStyle = node.color + '18';
                                ctx.fill();

                                // 2. SEMI-TRANSPARENT RING
                                ctx.beginPath();
                                ctx.arc(node.x, node.y, radius + 2 / globalScale, 0, 2 * Math.PI, false);
                                ctx.strokeStyle = node.color + '44';
                                ctx.stroke();

                                // 3. CORE CIRCLE
                                ctx.beginPath();
                                ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI, false);
                                ctx.fillStyle = node.color;
                                ctx.shadowBlur = 15 / globalScale;
                                ctx.shadowColor = node.color;
                                ctx.fill();
                                ctx.shadowBlur = 0;

                                // 4. TEXT LABEL (Professional positioning)
                                if (globalScale > 3) {
                                    const fontSize = 10 / globalScale;
                                    ctx.font = `bold ${fontSize}px Inter`;
                                    ctx.fillStyle = 'white';
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'top';
                                    ctx.fillText(label, node.x, node.y + radius + 3 / globalScale);
                                }
                            }}
                        />
                        <div className="absolute bottom-6 right-6 flex flex-col gap-2 pointer-events-none">
                            <div className="bg-slate-900/90 backdrop-blur px-4 py-2 rounded-xl border border-white/10 shadow-2xl">
                                <span className="text-[10px] font-black text-slate-500 uppercase block mb-1">Scale Resolution</span>
                                <span className="text-xs font-mono font-bold text-white">1:5000 GRID</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Metrics Column */}
                <div className="col-span-4 flex flex-col gap-6 min-h-0 overflow-hidden">

                    {/* Performance Metrics */}
                    <div className="grid grid-cols-2 gap-4">
                        <div className="glass p-6 rounded-3xl border border-white/5 bg-gradient-to-br from-red-500/10 to-transparent shadow-xl">
                            <div className="flex justify-between items-start mb-4">
                                <div className="p-2.5 bg-red-500/20 rounded-xl"><AlertTriangle className="text-red-500" size={24} /></div>
                                <span className="text-[10px] text-slate-500 font-black uppercase tracking-widest">Inundated</span>
                            </div>
                            <div className="flex items-baseline gap-2">
                                <div className="text-5xl font-black text-white leading-none">{currentStats.flooded_nodes}</div>
                                <div className="text-xs font-bold text-red-500/80">NODES</div>
                            </div>
                            <div className="mt-4 h-1.5 w-full bg-slate-900 rounded-full overflow-hidden border border-white/5">
                                <div className="h-full bg-red-500 transition-all duration-700 ease-out" style={{ width: `${Math.min((currentStats.flooded_nodes / (graphData.nodes.length || 1)) * 100, 100)}%` }}></div>
                            </div>
                        </div>

                        <div className="glass p-6 rounded-3xl border border-white/5 bg-gradient-to-br from-blue-500/10 to-transparent shadow-xl">
                            <div className="flex justify-between items-start mb-4">
                                <div className="p-2.5 bg-blue-500/20 rounded-xl"><Droplets className="text-blue-500" size={24} /></div>
                                <span className="text-[10px] text-slate-500 font-black uppercase tracking-widest">Discharge</span>
                            </div>
                            <div className="flex items-baseline gap-1">
                                <div className="text-5xl font-black text-white leading-none">{currentStats.total_flow?.toFixed(1)}</div>
                                <div className="text-xs font-bold text-blue-500/80 uppercase">m³/s</div>
                            </div>
                            <p className="text-[9px] font-bold text-slate-500 uppercase mt-4">Peak Volumetric Rate</p>
                        </div>

                        {/* NEW: Cascade Depth Card */}
                        <div className="glass p-6 rounded-3xl border border-white/5 bg-gradient-to-br from-amber-500/10 to-transparent shadow-xl">
                            <div className="flex justify-between items-start mb-4">
                                <div className="p-2.5 bg-amber-500/20 rounded-xl"><Activity className="text-amber-500" size={24} /></div>
                                <span className="text-[10px] text-slate-500 font-black uppercase tracking-widest">Cascade Depth</span>
                            </div>
                            <div className="flex items-baseline gap-2">
                                <div className="text-5xl font-black text-white leading-none">{currentStats.cascade_depth || 0}</div>
                                <div className="text-xs font-bold text-amber-500/80 uppercase">Hops</div>
                            </div>
                            <p className="text-[9px] font-bold text-slate-500 uppercase mt-4">Failure Chain Length ($\Lambda$)</p>
                        </div>

                        {/* NEW: Resilience Card */}
                        <div className="glass p-6 rounded-3xl border border-white/5 bg-gradient-to-br from-emerald-500/10 to-transparent shadow-xl">
                            <div className="flex justify-between items-start mb-4">
                                <div className="p-2.5 bg-emerald-500/20 rounded-xl"><RefreshCw className="text-emerald-500" size={24} /></div>
                                <span className="text-[10px] text-slate-500 font-black uppercase tracking-widest">Resilience</span>
                            </div>
                            <div className="flex items-baseline gap-2">
                                <div className="text-5xl font-black text-white leading-none">{(currentStats.resilience * 100).toFixed(0)}</div>
                                <div className="text-xs font-bold text-emerald-500/80 uppercase">%</div>
                            </div>
                            <p className="text-[9px] font-bold text-slate-500 uppercase mt-4">Network Integrity Score ($R$)</p>
                        </div>
                    </div>

                    {/* Propagation Chart - Professional Recharts */}
                    <div className="glass p-8 rounded-[2rem] flex-1 flex flex-col min-h-0 border border-white/5 shadow-2xl bg-slate-900/20 translate-y-0">
                        <div className="flex items-center justify-between border-b border-white/10 pb-6 mb-6">
                            <div className="flex items-center gap-3">
                                <BarChart3 size={20} className="text-emerald-400" />
                                <h3 className="font-black text-xs uppercase tracking-[0.2em] text-white">Temporal Dynamics</h3>
                                <span className="ml-2 w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
                            </div>
                            <span className="text-[9px] font-black text-slate-400 bg-white/5 px-3 py-1 rounded-lg border border-white/5">LIVE TELEMETRY</span>
                        </div>
                        <div className="flex-1 -mx-4">
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={allHistory.slice(0, currentIndex + 1)}>
                                    <defs>
                                        <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#ef4444" stopOpacity={0.6} />
                                            <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#ffffff05" vertical={false} />
                                    <XAxis dataKey="time" hide />
                                    <YAxis hide domain={[0, graphData.nodes.length || 'auto']} />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#020617', border: '1px solid #ffffff10', borderRadius: '16px', fontSize: '10px', boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.5)' }}
                                        labelStyle={{ display: 'none' }}
                                    />
                                    <Area
                                        type="stepAfter"
                                        dataKey="flooded_nodes"
                                        stroke="#ef4444"
                                        strokeWidth={4}
                                        fill="url(#chartGrad)"
                                        name="Critical Points"
                                        animationDuration={playbackSpeed}
                                    />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Diagnostics and Critical Nodes Panel */}
                    <div className="glass p-6 rounded-3xl border border-white/5 bg-slate-950/60 shadow-inner flex-1 flex flex-col min-h-0 overflow-hidden">
                        <div className="flex items-center gap-3 mb-6">
                            <div className="p-1.5 bg-emerald-500/10 rounded-lg"><Activity size={14} className="text-emerald-500" /></div>
                            <h4 className="text-[10px] font-black text-slate-200 uppercase tracking-[0.2em]">Engine Reliability</h4>
                        </div>

                        <div className="flex-1 overflow-y-auto pr-2 space-y-6 scrollbar-thin">
                            <div className="flex flex-col gap-1.5">
                                <div className="flex justify-between items-center text-[10px] font-black uppercase tracking-widest mb-1">
                                    <span className="text-slate-500">Node Failure Rate</span>
                                    <span className="text-red-400">{(currentStats.flooded_nodes / (graphData.nodes.length || 1) * 100).toFixed(0)}%</span>
                                </div>
                                <div className="h-1.5 w-full bg-slate-900 rounded-full overflow-hidden">
                                    <div className="h-full bg-red-400" style={{ width: `${(currentStats.flooded_nodes / (graphData.nodes.length || 1) * 100)}%` }}></div>
                                </div>
                            </div>

                            <div className="space-y-3">
                                <h5 className="text-[9px] font-black text-slate-500 uppercase tracking-widest">High-Impact Vulnerabilities</h5>
                                {graphData.nodes.slice(0, 5).map((node, i) => (
                                    <div key={node.id} className="flex items-center justify-between bg-slate-900/40 p-3 rounded-xl border border-white/5">
                                        <div className="flex items-center gap-3">
                                            <div className="w-1.5 h-1.5 rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.5)]"></div>
                                            <span className="text-[10px] font-mono text-slate-300">NODE_{node.id.slice(-4)}</span>
                                        </div>
                                        <span className="text-[10px] font-black text-blue-400">RANK #{i + 1}</span>
                                    </div>
                                ))}
                            </div>

                            <div className="flex justify-between items-center bg-slate-900/50 p-3 rounded-xl border border-white/5">
                                <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest italic">Simulation Status</span>
                                <span className={`text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-md ${isPlaying ? 'bg-amber-500/20 text-amber-400 shadow-[0_0_12px_rgba(245,158,11,0.2)]' : (currentIndex > 0 ? 'bg-blue-500/20 text-blue-400' : 'bg-emerald-500/20 text-emerald-400')}`}>
                                    {isPlaying ? 'Computing...' : (currentIndex > 0 ? 'Step Paused' : 'Ready')}
                                </span>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default App;
