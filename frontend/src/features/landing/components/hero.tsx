const Hero = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center pt-20">
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 hero-gradient z-10"></div>
        <div
          className="w-full h-full bg-cover bg-center"
          data-alt="Dark cinematic movie theater background image"
          style={{
            backgroundImage:
              "url('https://lh3.googleusercontent.com/aida-public/AB6AXuCbuomlqjv7wdQmDkyqxIGIKsLNKqAQdWN3W1QwJ1ZgRLlSQss3bhTSWZXMSbY4NEpd8LF0vIPiNI5MQ4kip4E_yADnmpY--Mkwk8HvH5Ig_2zBkhWGsB3Ercd_H7BMzTw2jfYaloxUA382TLby1vZEliq2JEzZYeYJ1gLf9O15f_uHjS6N7s0FtftaJ4wMx6sYHJPQ5G7LvXY_VcZbgOq8-Kn368SGY7EF6ryQs5bQzHhl1-MMNQB89VD5KnAmos1ATb3-M6wEEaA')",
          }}
        ></div>
      </div>
      <div className="relative z-20 max-w-240 mx-auto px-6 text-center">
        <h1 className="text-white text-5xl md:text-7xl font-black leading-tight tracking-tight mb-6">
          Unlimited movies, TV shows, and more
        </h1>
        <p className="text-white/80 text-lg md:text-2xl font-normal mb-10 max-w-2xl mx-auto">
          Watch anywhere. Cancel anytime. Ready to watch? Enter your email to
          create or restart your membership.
        </p>
        <div className="flex flex-col md:flex-row items-center justify-center gap-3">
          <input
            className="w-full md:w-96 h-14 rounded-lg bg-black/40 border border-white/20 px-4 text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="Email address"
            type="email"
          />
          <button className="w-full md:w-auto bg-primary text-white px-8 h-14 rounded-lg text-xl font-bold flex items-center justify-center gap-2 hover:bg-primary/90 transition-all group">
            Get Started
            <span className="material-symbols-outlined group-hover:translate-x-1 transition-transform">
              chevron_right
            </span>
          </button>
        </div>
      </div>
    </section>
  )
}

export default Hero
