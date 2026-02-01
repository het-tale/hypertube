const FeaturesSection = () => {
    return (
        <section className="bg-background-dark py-24 border-y border-white/5">
<div className="max-w-300 mx-auto px-6">
<div className="mb-16">
<h2 className="text-white text-4xl font-black tracking-tight mb-4">Why choose Hypertube?</h2>
<p className="text-gray-400 text-lg">Experience the best in video streaming with our premium features.</p>
</div>
<div className="grid grid-cols-1 md:grid-cols-3 gap-8">

<div className="flex flex-col gap-5 p-8 rounded-xl bg-white/5 border border-white/10 hover:border-primary/50 transition-colors group">
<div className="text-primary">
<span className="material-symbols-outlined text-4xl! group-hover:scale-110 transition-transform">play_circle</span>
</div>
<div className="flex flex-col gap-2">
<h3 className="text-white text-xl font-bold">Stream Instantly</h3>
<p className="text-gray-400 leading-relaxed">Watch on any device in high definition with seamless playback and no buffering.</p>
</div>
</div>

<div className="flex flex-col gap-5 p-8 rounded-xl bg-white/5 border border-white/10 hover:border-primary/50 transition-colors group">
<div className="text-primary">
<span className="material-symbols-outlined text-4xl! group-hover:scale-110 transition-transform">shield</span>
</div>
<div className="flex flex-col gap-2">
<h3 className="text-white text-xl font-bold">Legal &amp; Safe</h3>
<p className="text-gray-400 leading-relaxed">Fully licensed content from the world's biggest studios for a worry-free experience.</p>
</div>
</div>

<div className="flex flex-col gap-5 p-8 rounded-xl bg-white/5 border border-white/10 hover:border-primary/50 transition-colors group">
<div className="text-primary">
<span className="material-symbols-outlined text-4xl! group-hover:scale-110 transition-transform">globe</span>
</div>
<div className="flex flex-col gap-2">
<h3 className="text-white text-xl font-bold">Multi-Language Support</h3>
<p className="text-gray-400 leading-relaxed">Subtitles and professional audio dubbing in over 20+ languages available for all titles.</p>
</div>
</div>
</div>
</div>
</section>
    )
}

export default FeaturesSection