import React, { useState, useRef } from 'react';
import { motion, useScroll, useTransform, useSpring } from 'framer-motion';
import {
  Shield,
  ArrowRight,
  TrendingUp,
  AlertTriangle,
  Cpu,
  Layers,
  Database,
  Sliders,
  Workflow,
  Sparkles,
  Lock,
  CheckCircle2,
  Play,
  Activity,
  Zap,
  Network,
  Maximize2,
  Compass,
} from 'lucide-react';
import GlowButton from '@/components/GlowButton';
import GlowCard from '@/components/GlowCard';
import GlowCursor from '@/animations/GlowCursor';
import HeroGlowBackground from '@/backgrounds/HeroGlowBackground';
import ScrollTimelineGlow from '@/components/ScrollTimelineGlow';
import RevenueForecastChart from '@/charts/RevenueForecastChart';
import AnomalyTimeline from '@/charts/AnomalyTimeline';
import HeatmapChart from '@/charts/HeatmapChart';
import ScenarioComparisonChart from '@/charts/ScenarioComparisonChart';
import { DEMO_BUSINESSES } from '@/api/demoApi';

interface LandingPageProps {
  onNavigate: (path: string) => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onNavigate }) => {
  const [selectedDemo, setSelectedDemo] = useState(DEMO_BUSINESSES[0]);
  const timelineRef = useRef<HTMLDivElement>(null);

  // Framer Motion scroll telemetry
  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, { stiffness: 120, damping: 28, restDelta: 0.001 });
  const bgGlowY = useTransform(scrollYProgress, [0, 1], [0, 260]);
  const heroOpacity = useTransform(scrollYProgress, [0, 0.25], [1, 0.85]);

  // Simulation preview interactive state
  const [simPrice, setSimPrice] = useState(5);
  const [simMarketing, setSimMarketing] = useState(-8);
  const [simInventory, setSimInventory] = useState(10);

  const calculatedRevenue = Number((148.24 * (1 + (simPrice * 0.8 + simMarketing * 0.3) / 100)).toFixed(1));
  const calculatedProfit = Number((21.05 * (1 + (simPrice * 1.4 - simMarketing * 0.25) / 100)).toFixed(1));
  const calculatedRisk = Math.max(20, Math.min(95, Math.round(74 - simPrice * 1.2 + simMarketing * 0.5 - simInventory * 0.8)));

  return (
    <div className="relative min-h-screen bg-[#050302] text-[#F5F0EA] overflow-x-hidden selection:bg-[#FF6A00]/30 selection:text-[#FFB15A]">
      {/* Scroll Progress Glow Bar */}
      <motion.div
        className="fixed top-0 left-0 right-0 h-[2.5px] bg-gradient-to-r from-[#FF6A00] via-[#FF8A24] to-[#FFB15A] origin-left z-50 shadow-[0_0_12px_#FF6A00]"
        style={{ scaleX }}
      />

      {/* 1. Official WebGL Glow Cursor */}
      <div className="hidden lg:block">
        <GlowCursor
          color="#FF6A00"
          secondaryColor="#FFB15A"
          intensity={2.2}
          trailWidth={7}
          linger={0.82}
          glow={1.4}
          hotspot={0.72}
          followSpeed={0.18}
          grain={0.03}
          clickBurst={true}
          quality="high"
          theme="dark"
          blendMode="screen"
          maxDevicePixelRatio={1.5}
          enabled={true}
        />
      </div>

      {/* 2. Top Orange Light Reservoir with Scroll Motion Parallax */}
      <motion.div
        className="fixed top-[-10%] left-1/2 -translate-x-1/2 w-[1200px] h-[650px] rounded-full pointer-events-none blur-[160px] opacity-50 z-0"
        style={{
          y: bgGlowY,
          background: 'radial-gradient(circle, rgba(255,106,0,0.65) 0%, rgba(217,91,0,0.3) 45%, transparent 75%)',
        }}
      />

      {/* 3. Global Ambient Floating Particles & Micro-Grid */}
      <div className="fixed inset-0 grid-pattern pointer-events-none opacity-30 z-0" />

      {/* 4. STICKY TOP NAVIGATION */}
      <nav className="sticky top-0 z-40 w-full border-b border-[#FF6A00]/20 bg-[#050302]/85 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          {/* Logo */}
          <div
            onClick={() => onNavigate('/')}
            className="flex items-center gap-3 cursor-pointer group"
          >
            <div className="w-9 h-9 rounded-md bg-gradient-to-br from-[#FF6A00] to-[#FF8A24] p-1.5 flex items-center justify-center shadow-[0_0_20px_rgba(255,106,0,0.6)] group-hover:shadow-[0_0_30px_rgba(255,106,0,0.9)] transition-all">
              <svg viewBox="0 0 100 100" className="w-full h-full fill-white">
                <polygon points="50,10 90,85 10,85" />
              </svg>
            </div>
            <div className="flex flex-col">
              <span className="font-extrabold tracking-widest text-[#F5F0EA] text-lg leading-none font-sans">
                AEGIS
              </span>
              <span className="text-[9px] font-mono tracking-widest text-[#FF8A24] mt-0.5">
                AI RISK INTELLIGENCE
              </span>
            </div>
          </div>

          {/* Center Navigation Links */}
          <div className="hidden md:flex items-center gap-8 text-xs font-mono text-[#A89D92]">
            <a href="#platform" className="hover:text-[#FFB15A] transition-colors">
              Platform
            </a>
            <a href="#intelligence" className="hover:text-[#FFB15A] transition-colors">
              Intelligence
            </a>
            <a href="#risk" className="hover:text-[#FFB15A] transition-colors">
              Risk
            </a>
            <a href="#simulation" className="hover:text-[#FFB15A] transition-colors">
              Simulation
            </a>
            <a href="#how-it-works" className="hover:text-[#FFB15A] transition-colors">
              How It Works
            </a>
          </div>

          {/* Right Action CTAs */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => onNavigate('/docs')}
              className="hidden sm:inline-block text-xs font-mono text-[#A89D92] hover:text-[#F5F0EA] transition-colors"
            >
              Documentation
            </button>
            <GlowButton
              variant="secondary"
              size="sm"
              onClick={() => onNavigate('/demo')}
            >
              Explore Demo
            </GlowButton>
            <GlowButton
              variant="primary"
              size="sm"
              onClick={() => onNavigate('/signup')}
            >
              Get Started Now
            </GlowButton>
          </div>
        </div>
      </nav>

      {/* 5. HERO SECTION - CLEAN, CINEMATIC, NO GLOBE, NO TYPE-SOMETHING BADGE */}
      <motion.section
        style={{ opacity: heroOpacity }}
        className="relative pt-24 pb-20 px-6 max-w-7xl mx-auto overflow-visible z-10"
      >
        <HeroGlowBackground showLightning={true} />

        <div className="relative z-10 flex flex-col items-center text-center max-w-4xl mx-auto space-y-8">
          {/* Main Editorial Headline with Italic Serif Accent matching Reference */}
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className="text-5xl sm:text-7xl lg:text-8xl font-extrabold tracking-tight leading-[1.05] text-[#F5F0EA]"
          >
            Launch <span className="font-editorial-italic font-normal text-[#FF8A24]">faster.</span> <br />
            Convert <span className="font-editorial-italic font-normal text-[#FFB15A]">better.</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.15, ease: [0.16, 1, 0.3, 1] }}
            className="text-base sm:text-xl text-[#A89D92] max-w-2xl mx-auto leading-relaxed font-sans"
          >
            See the risk <span className="font-editorial-italic text-[#FF8A24] font-normal">before</span> it becomes the loss. AEGIS turns fragmented business records into predictive forecasts, threat telemetry, and actionable decisions.
          </motion.p>

          {/* CTAs with normal square rounded-lg styling */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className="pt-2 flex flex-wrap justify-center items-center gap-4"
          >
            <GlowButton
              size="lg"
              showArrow
              onClick={() => onNavigate('/demo')}
            >
              Get Started Now
            </GlowButton>
            <GlowButton
              variant="secondary"
              size="lg"
              onClick={() => onNavigate('/command-center')}
            >
              Explore Live Features
            </GlowButton>
          </motion.div>

          {/* Trusted Companies Bar Matching Reference Image 1 */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1, delay: 0.45 }}
            className="pt-12 flex flex-col items-center space-y-4"
          >
            <span className="text-xs font-mono text-[#6F665F] tracking-widest uppercase">
              Trusted by 100+ Startups & Enterprise Teams worldwide
            </span>
            <div className="flex flex-wrap items-center justify-center gap-8 text-[#A89D92]/60 font-mono text-xs">
              <span className="hover:text-[#FFB15A] transition-colors">✦ CHANCE</span>
              <span className="hover:text-[#FFB15A] transition-colors">✦ PromptPilot</span>
              <span className="hover:text-[#FFB15A] transition-colors">❯❯❯ Screen</span>
              <span className="hover:text-[#FFB15A] transition-colors">✦ EverMist</span>
              <span className="hover:text-[#FFB15A] transition-colors">✦ Tasky</span>
            </div>
          </motion.div>
        </div>
      </motion.section>

      {/* 6. TRUST / DATA STRIP WITH TRANSPARENT AMBIENT FLOW */}
      <motion.section
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-50px' }}
        transition={{ duration: 0.7 }}
        className="relative z-10 border-t border-[#FF6A00]/15 bg-transparent py-10 px-6"
      >
        <div className="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-5 gap-8 text-center font-mono">
          <div>
            <div className="text-3xl font-extrabold text-[#FF6A00]">15</div>
            <div className="text-xs text-[#A89D92] mt-1">Synthetic Environments</div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-[#FF8A24]">100%</div>
            <div className="text-xs text-[#A89D92] mt-1">Multi-Tenant Scoped</div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-[#FFB15A]">Python</div>
            <div className="text-xs text-[#A89D92] mt-1">First Intelligence Engine</div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-[#F5F0EA]">&lt;10ms</div>
            <div className="text-xs text-[#A89D92] mt-1">Causal Graph Traversal</div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-[#FF8A24]">$12.4M</div>
            <div className="text-xs text-[#A89D92] mt-1">Exposure Mitigated</div>
          </div>
        </div>
      </motion.section>

      {/* GLOWING SCROLL TIMELINE THAT TRAVELS DOWN AS YOU SCROLL */}
      <div ref={timelineRef} className="relative w-full overflow-visible">
        <ScrollTimelineGlow containerRef={timelineRef} className="hidden lg:block" />

        {/* 7. PLATFORM INTELLIGENCE LAYER */}
        <section id="platform" className="relative w-full py-24 px-6 overflow-hidden z-10">
          <div className="max-w-7xl mx-auto relative z-10">
            <motion.div
              initial={{ opacity: 0, y: 35 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-60px' }}
              transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
              className="text-center max-w-3xl mx-auto mb-16 space-y-2 relative z-10"
            >
              <span className="font-fullwidth-accent text-xs text-[#FF8A24] font-semibold tracking-wider">
              WHY CLIENTS STICK WITH US
            </span>
            <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-[#F5F0EA]">
              One intelligence layer <br />
              <span className="font-editorial-italic font-normal text-[#FFB15A]">for the entire</span> enterprise.
            </h2>
            <p className="text-sm sm:text-base text-[#A89D92] max-w-xl mx-auto">
              We combine clarity, telemetry, and high-performing AI intelligence to deliver business outcomes that actually matter.
            </p>
          </motion.div>

        {/* 4 Feature Cards with Internal Orange Glow & 3D Interactive Hover Tilt */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 relative z-10">
          {/* Card 1: Implementation and tools */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-40px' }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <GlowCard
              className="p-8 min-h-[340px] flex flex-col justify-between"
              internalGlow={true}
              enableTilt={true}
              maxTilt={12}
            >
              <div>
                <h3 className="text-2xl font-bold text-[#F5F0EA] font-sans">
                  Implementation <br />
                  <span className="font-editorial-italic font-normal text-[#FFB15A]">and tools</span>
                </h3>
                <p className="text-xs text-[#A89D92] mt-2 max-w-xs leading-relaxed">
                  Seamless data pipelines connecting with the right tools to keep you alert and ahead.
                </p>
              </div>

              {/* Radiant Orange Internal Pedestal Emblem */}
              <div className="relative mt-8 h-40 flex items-center justify-center">
                <div className="absolute bottom-0 w-48 h-24 rounded-t-full bg-gradient-to-t from-[#FF6A00] to-transparent blur-xl opacity-60" />
                <div className="relative z-10 w-20 h-20 rounded-md bg-[#17100B] border-2 border-[#FF8A24] flex items-center justify-center shadow-[0_0_35px_rgba(255,106,0,0.8)]">
                  <Shield className="w-10 h-10 text-[#FFB15A] fill-[#FF6A00]/30" />
                </div>
              </div>
            </GlowCard>
          </motion.div>

          {/* Card 2: High-converting */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-40px' }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <GlowCard
              className="p-8 min-h-[340px] flex flex-col justify-between"
              internalGlow={true}
              enableTilt={true}
              maxTilt={12}
            >
              <div>
                <h3 className="text-2xl font-bold text-[#F5F0EA] font-sans">
                  High-converting <br />
                  <span className="font-editorial-italic font-normal text-[#FF8A24]">intelligence</span>
                </h3>
                <p className="text-xs text-[#A89D92] mt-2 max-w-xs leading-relaxed">
                  Clear decisions that convert risk signals into strategic capital growth and operational margin.
                </p>
              </div>

              {/* Glowing Lightning / Electric Core inside card */}
              <div className="relative mt-8 h-40 flex items-center justify-center">
                <div className="absolute bottom-0 w-48 h-24 rounded-t-full bg-gradient-to-t from-[#FF8A24] to-transparent blur-xl opacity-60" />
                <div className="relative z-10 w-20 h-20 rounded-md bg-[#17100B] border-2 border-[#FFB15A] flex items-center justify-center shadow-[0_0_35px_rgba(255,177,90,0.8)]">
                  <Zap className="w-10 h-10 text-[#FFB15A] fill-[#FFB15A]/30" />
                </div>
              </div>
            </GlowCard>
          </motion.div>

          {/* Card 3: Maximum Return on ROI */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-40px' }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <GlowCard
              className="p-8 min-h-[340px] flex flex-col justify-between"
              internalGlow={true}
              enableTilt={true}
              maxTilt={12}
            >
              <div>
                <h3 className="text-2xl font-bold text-[#F5F0EA] font-sans">
                  Maximum Return <br />
                  <span className="font-editorial-italic font-normal text-[#FFB15A]">on ROI</span>
                </h3>
                <p className="text-xs text-[#A89D92] mt-2 max-w-xs leading-relaxed">
                  Prioritize decisions with high expected ROI and minimal implementation friction.
                </p>
              </div>

              {/* Concentric Step Pedestal inside card */}
              <div className="relative mt-8 h-40 flex flex-col items-center justify-end pb-2">
                <div className="absolute bottom-0 w-56 h-28 rounded-t-full bg-gradient-to-t from-[#FF6A00] to-transparent blur-2xl opacity-75" />
                <div className="relative z-10 text-center font-mono">
                  <span className="text-xs text-[#FFB15A] tracking-wider block">RETURN ON RISK</span>
                  <span className="text-3xl font-extrabold text-white text-glow-bright">+120%</span>
                </div>
              </div>
            </GlowCard>
          </motion.div>

          {/* Card 4: Clear steps and trust */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-40px' }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <GlowCard
              className="p-8 min-h-[340px] flex flex-col justify-between"
              internalGlow={true}
              enableTilt={true}
              maxTilt={12}
            >
              <div>
                <h3 className="text-2xl font-bold text-[#F5F0EA] font-sans">
                  Clear steps <br />
                  <span className="font-editorial-italic font-normal text-[#FF8A24]">and trust</span>
                </h3>
                <p className="text-xs text-[#A89D92] mt-2 max-w-xs leading-relaxed">
                  Step-by-step causal investigation with complete auditability for corporate governance.
                </p>
              </div>

              {/* Tiered Glowing Pyramid inside card */}
              <div className="relative mt-8 h-40 flex flex-col items-center justify-end pb-2 space-y-1.5">
                <div className="absolute bottom-0 w-52 h-28 rounded-t-full bg-gradient-to-t from-[#FF6A00] to-transparent blur-2xl opacity-75" />
                <div className="w-16 h-2.5 rounded-sm bg-[#FFB15A] shadow-[0_0_12px_#FFB15A] z-10" />
                <div className="w-28 h-2.5 rounded-sm bg-[#FF8A24] shadow-[0_0_10px_#FF8A24] z-10" />
                <div className="w-40 h-3 rounded-sm bg-[#FF6A00] shadow-[0_0_8px_#FF6A00] z-10" />
              </div>
            </GlowCard>
          </motion.div>
        </div>
        </div>
      </section>

      {/* 8. THE PROCESS: FAST, CLEAR, DONE */}
      <motion.section
        id="how-it-works"
        initial={{ opacity: 0, y: 35 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-60px' }}
        transition={{ duration: 0.7 }}
        className="py-24 px-6 max-w-7xl mx-auto border-t border-[#FF6A00]/20 relative z-10"
      >
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-2">
          <span className="font-fullwidth-accent text-xs text-[#FF8A24] font-semibold">
            THE PROCESS FAST, CLEAR, DONE
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-[#F5F0EA]">
            No endless configurations. Just intelligence that works.
          </h2>
        </div>

        {/* 3 Step Cards with Tilt & Internal Glowing Spheres */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            {
              title: 'Share Your Vision',
              sub: 'Upload your business ZIP or connect data source in under 60 seconds.',
              step: '01',
            },
            {
              title: 'We Model It',
              sub: 'Automated canonical schema mapping and multi-horizon forecasting.',
              step: '02',
            },
            {
              title: 'Ready to Decide',
              sub: 'Continuous monitoring, threat detection, and simulated decisions.',
              step: '03',
            },
          ].map((item, idx) => (
            <motion.div
              key={item.step}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-40px' }}
              transition={{ duration: 0.6, delay: idx * 0.15 }}
            >
              <GlowCard
                className="p-8 min-h-[300px] flex flex-col justify-between"
                internalGlow={true}
                enableTilt={true}
                maxTilt={12}
              >
                <div>
                  <span className="text-xs font-mono text-[#FF8A24] font-bold block mb-1">STAGE {item.step}</span>
                  <h3 className="text-xl font-bold text-[#F5F0EA]">{item.title}</h3>
                  <p className="text-xs text-[#A89D92] mt-2 leading-relaxed">{item.sub}</p>
                </div>

                {/* Glowing internal sphere */}
                <div className="relative mt-6 h-28 flex items-center justify-center">
                  <div className="w-24 h-24 rounded-full bg-gradient-to-t from-[#FF6A00] to-[#FFB15A] opacity-80 blur-md flex items-center justify-center shadow-[0_0_30px_#FF6A00]" />
                  <div className="absolute w-12 h-12 rounded-full bg-[#120C08] border border-white/40 flex items-center justify-center z-10">
                    <CheckCircle2 className="w-6 h-6 text-[#FFB15A]" />
                  </div>
                </div>
              </GlowCard>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* 9. INTERACTIVE FORECASTING & ANOMALY PREVIEW */}
      <motion.section
        id="intelligence"
        initial={{ opacity: 0, y: 35 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-60px' }}
        transition={{ duration: 0.7 }}
        className="py-24 px-6 max-w-7xl mx-auto border-t border-[#FF6A00]/20 relative z-10"
      >
        <div className="mb-12">
          <span className="font-fullwidth-accent text-xs text-[#FF8A24] font-semibold">
            PREDICTIVE TELEMETRY
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-[#F5F0EA] mt-1">
            Machine intelligence trained on your business dynamics
          </h2>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-7">
            <GlowCard className="flex flex-col justify-between h-full" internalGlow={true} enableTilt={true} maxTilt={8}>
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-bold text-[#F5F0EA]">90-Day Enterprise Topline Forecast</h3>
                    <p className="text-xs text-[#A89D92] font-mono">Ensemble LightGBM + Prophet • 94% Confidence</p>
                  </div>
                  <span className="px-3 py-1 rounded-md bg-[#FF6A00]/20 text-[#FFB15A] text-xs font-mono font-semibold border border-[#FF6A00]/30">
                    +$6.4M Q2 Outlook
                  </span>
                </div>
                <RevenueForecastChart height={280} />
              </div>
            </GlowCard>
          </div>

          <div className="lg:col-span-5">
            <GlowCard className="flex flex-col justify-between h-full" internalGlow={true} enableTilt={true} maxTilt={8}>
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-bold text-[#F5F0EA]">Real-Time Anomaly Stream</h3>
                    <p className="text-xs text-[#A89D92] font-mono">Isolation Forest & LOF Outlier Detection</p>
                  </div>
                  <span className="w-2.5 h-2.5 rounded-full bg-[#FF4500] animate-ping" />
                </div>
                <AnomalyTimeline />
              </div>
            </GlowCard>
          </div>
        </div>
      </motion.section>

      {/* 10. RISK MATRIX SECTION */}
      <motion.section
        id="risk"
        initial={{ opacity: 0, y: 35 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-60px' }}
        transition={{ duration: 0.7 }}
        className="py-24 px-6 max-w-7xl mx-auto border-t border-[#FF6A00]/20 relative z-10"
      >
        <div className="mb-12">
          <span className="font-fullwidth-accent text-xs text-[#FF8A24] font-semibold">
            THREAT EXPOSURE RADAR
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-[#F5F0EA] mt-1">
            Probability × Impact × Exposure
          </h2>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-8">
            <GlowCard internalGlow={true} enableTilt={true} maxTilt={8}>
              <h4 className="text-base font-bold text-[#F5F0EA] mb-4">Threat Exposure Scatter Matrix</h4>
              <HeatmapChart height={320} />
            </GlowCard>
          </div>

          <div className="lg:col-span-4">
            <GlowCard className="flex flex-col justify-between h-full" internalGlow={true} enableTilt={true} maxTilt={8}>
              <div>
                <div className="flex items-center gap-2 text-xs font-mono text-[#FF4500] font-bold">
                  <AlertTriangle className="w-4 h-4 text-[#FF6A00]" />
                  <span>CRITICAL ACTIVE THREAT</span>
                </div>
                <h3 className="text-xl font-bold text-[#F5F0EA] mt-2">Diesel Benchmark Price Surge</h3>
                <p className="text-xs text-[#A89D92] mt-2 leading-relaxed">
                  Wholesale diesel benchmark spike (+28%) causing compounding operating margin erosion across cross-border highway corridors.
                </p>

                <div className="mt-6 p-4 rounded-lg bg-[#080604] border border-[#FF6A00]/20 space-y-2 text-xs font-mono">
                  <div className="flex justify-between">
                    <span className="text-[#6F665F]">Capital Exposure:</span>
                    <span className="text-[#FFB15A] font-bold">$2.85M</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#6F665F]">Confidence Score:</span>
                    <span className="text-[#FF8A24]">92%</span>
                  </div>
                </div>
              </div>

              <div className="pt-4 mt-6 border-t border-[#FF6A00]/14">
                <GlowButton
                  size="sm"
                  className="w-full"
                  onClick={() => onNavigate('/risk-center')}
                >
                  Inspect Threat Vector
                </GlowButton>
              </div>
            </GlowCard>
          </div>
        </div>
      </motion.section>

      {/* 11. WHAT-IF SIMULATION SECTION */}
      <motion.section
        id="simulation"
        initial={{ opacity: 0, y: 35 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-60px' }}
        transition={{ duration: 0.7 }}
        className="py-24 px-6 max-w-7xl mx-auto border-t border-[#FF6A00]/20 relative z-10"
      >
        <div className="mb-12">
          <span className="font-fullwidth-accent text-xs text-[#FF8A24] font-semibold">
            WHAT-IF SIMULATION ENGINE
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-[#F5F0EA] mt-1">
            Simulate business decisions before committing capital
          </h2>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
          <div className="lg:col-span-5">
            <GlowCard className="space-y-6" internalGlow={true} enableTilt={true} maxTilt={8}>
              <h4 className="text-base font-bold text-[#F5F0EA]">Simulation Levers</h4>

              <div>
                <div className="flex justify-between text-xs font-mono mb-2">
                  <span className="text-[#A89D92]">Price Adjustment</span>
                  <span className="text-[#FFB15A] font-bold">+{simPrice}%</span>
                </div>
                <input
                  type="range"
                  min="-10"
                  max="25"
                  value={simPrice}
                  onChange={(e) => setSimPrice(Number(e.target.value))}
                  className="w-full accent-[#FF6A00] cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs font-mono mb-2">
                  <span className="text-[#A89D92]">Marketing Budget Shift</span>
                  <span className="text-[#FF8A24] font-bold">{simMarketing}%</span>
                </div>
                <input
                  type="range"
                  min="-30"
                  max="30"
                  value={simMarketing}
                  onChange={(e) => setSimMarketing(Number(e.target.value))}
                  className="w-full accent-[#FF6A00] cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs font-mono mb-2">
                  <span className="text-[#A89D92]">Inventory Safety Buffer</span>
                  <span className="text-[#FFB15A] font-bold">+{simInventory}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="40"
                  value={simInventory}
                  onChange={(e) => setSimInventory(Number(e.target.value))}
                  className="w-full accent-[#FF6A00] cursor-pointer"
                />
              </div>

              <div className="pt-2">
                <GlowButton
                  size="md"
                  className="w-full"
                  onClick={() => onNavigate('/simulation')}
                >
                  Open Full Scenario Studio
                </GlowButton>
              </div>
            </GlowCard>
          </div>

          <div className="lg:col-span-7">
            <GlowCard className="space-y-6" internalGlow={true} enableTilt={true} maxTilt={8}>
              <div className="flex items-center justify-between">
                <h4 className="text-base font-bold text-[#F5F0EA]">Simulated Projected Delta</h4>
                <span className="text-xs font-mono text-[#FF8A24]">Active Scenario #S-2026</span>
              </div>

              <div className="grid grid-cols-3 gap-4 font-mono text-center">
                <div className="p-4 rounded-lg bg-[#080604] border border-[#FF6A00]/20">
                  <p className="text-[10px] text-[#6F665F] uppercase">Revenue</p>
                  <p className="text-2xl font-bold text-[#FFB15A] mt-1">${calculatedRevenue}M</p>
                  <p className="text-[10px] text-[#FF8A24] mt-0.5">vs $148.2M Baseline</p>
                </div>

                <div className="p-4 rounded-lg bg-[#080604] border border-[#FF6A00]/20">
                  <p className="text-[10px] text-[#6F665F] uppercase">Profit</p>
                  <p className="text-2xl font-bold text-[#F5F0EA] mt-1">${calculatedProfit}M</p>
                  <p className="text-[10px] text-[#FF8A24] mt-0.5">vs $21.0M Baseline</p>
                </div>

                <div className="p-4 rounded-lg bg-[#080604] border border-[#FF6A00]/20">
                  <p className="text-[10px] text-[#6F665F] uppercase">Risk Score</p>
                  <p className="text-2xl font-bold text-[#FF6A00] mt-1">{calculatedRisk} / 100</p>
                  <p className="text-[10px] text-[#A89D92] mt-0.5">Exposure Delta</p>
                </div>
              </div>

              <ScenarioComparisonChart
                baselineRevenue={148.2}
                simulatedRevenue={calculatedRevenue}
                baselineProfit={21.0}
                simulatedProfit={calculatedProfit}
                height={220}
              />
            </GlowCard>
          </div>
        </div>
      </motion.section>

      {/* 12. PRE-LOADED 15 DEMO ENVIRONMENTS WITH 3D TILT CARDS */}
      <motion.section
        initial={{ opacity: 0, y: 35 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-60px' }}
        transition={{ duration: 0.7 }}
        className="py-24 px-6 max-w-7xl mx-auto border-t border-[#FF6A00]/20 relative z-10"
      >
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-2">
          <span className="font-fullwidth-accent text-xs text-[#FF8A24] font-semibold">
            15 SYNTHETIC BUSINESS TWINS
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-[#F5F0EA]">
            Ready-to-Explore Enterprise Sandboxes
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {DEMO_BUSINESSES.slice(0, 10).map((b) => (
            <GlowCard
              key={b.id}
              onClick={() => {
                setSelectedDemo(b);
                onNavigate('/command-center');
              }}
              enableTilt={true}
              maxTilt={14}
              internalGlow={true}
              className="p-5 flex flex-col justify-between cursor-pointer"
            >
              <div>
                <span className="text-[11px] font-mono text-[#FF8A24] block">{b.industry}</span>
                <h4 className="text-base font-bold text-[#F5F0EA] mt-1">{b.name}</h4>
                <p className="text-xs text-[#A89D92] mt-1.5 line-clamp-2">{b.description}</p>
              </div>
              <div className="mt-5 pt-3 border-t border-[#FF6A00]/12 flex items-center justify-between text-xs font-mono">
                <span className="text-[#FFB15A] font-bold">{b.metrics.revenue}</span>
                <span className="text-[#A89D92]">{b.healthScore} Health</span>
              </div>
            </GlowCard>
          ))}
        </div>

        <div className="text-center mt-10">
          <GlowButton
            variant="secondary"
            size="md"
            showArrow
            onClick={() => onNavigate('/demo')}
          >
            Explore All 15 Environments & Scenarios
          </GlowButton>
        </div>
      </motion.section>
      </div>

      {/* 13. FOOTER BANNER MATCHING VELOCITY REFERENCE IN IMAGE 1 */}
      <motion.section
        initial={{ opacity: 0, y: 35 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-60px' }}
        transition={{ duration: 0.7 }}
        className="py-20 px-6 border-t border-[#FF6A00]/20 relative z-10 overflow-hidden"
      >
        <div className="max-w-6xl mx-auto rounded-2xl bg-[#0C0805] border border-[#FF6A00]/40 p-12 relative overflow-hidden shadow-[0_0_60px_rgba(255,106,0,0.35)]">
          {/* Internal Right Radiant Sunset Bloom */}
          <div
            className="absolute right-0 top-0 bottom-0 w-[550px] blur-[90px] opacity-75 pointer-events-none"
            style={{
              background: 'radial-gradient(circle at 100% 50%, #FF6A00 0%, #FF8A24 40%, transparent 80%)',
            }}
          />

          <div className="relative z-10 max-w-xl space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-md bg-[#FF6A00] flex items-center justify-center font-bold text-white text-sm">
                ▲
              </div>
              <span className="text-xl font-extrabold text-white tracking-wider font-sans">AEGIS</span>
            </div>
            <h3 className="text-2xl sm:text-4xl font-extrabold text-[#F5F0EA] leading-tight">
              Ready to deploy intelligence that actually delivers?
            </h3>
            <p className="text-xs sm:text-sm text-[#A89D92]">
              Let AEGIS synchronize your enterprise data, forecast trends, and mitigate risks before they impact capital.
            </p>
            <div className="pt-2">
              <GlowButton
                size="md"
                showArrow
                onClick={() => onNavigate('/signup')}
              >
                Get Started Now
              </GlowButton>
            </div>
          </div>
        </div>
      </motion.section>

      {/* 14. BASE FOOTER */}
      <footer className="border-t border-[#FF6A00]/14 py-8 px-6 bg-[#050302] text-xs font-mono text-[#6F665F] relative z-10">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>© 2026 AEGIS Autonomous Risk Intelligence Platform. All rights reserved.</div>
          <div className="flex items-center gap-6">
            <a href="#platform" className="hover:text-[#FFB15A] transition-colors">Platform</a>
            <a href="#risk" className="hover:text-[#FFB15A] transition-colors">Risk Engine</a>
            <a href="#how-it-works" className="hover:text-[#FFB15A] transition-colors">Pipeline</a>
            <a href="#simulation" className="hover:text-[#FFB15A] transition-colors">Simulation</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
