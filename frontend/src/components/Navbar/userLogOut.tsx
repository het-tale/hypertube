const UserLogedOutNavbar = () => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass-nav border-b border-white/10">
      <div className="max-w-300 mx-auto px-6 h-20 flex items-center justify-between">
        <div className="flex items-center gap-3 text-primary">
          <div className="size-8 bg-primary rounded-lg flex items-center justify-center text-white">
            <span className="material-symbols-outlined text-2xl!">
              play_circle
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            Hypertube
          </h1>
        </div>
        <div className="flex items-center gap-4">
          <button
            className="px-5 h-10 text-sm font-bold hover:text-primary transition-colors"
          >
            Login
          </button>
          <button className="bg-primary text-white px-6 h-10 rounded-lg text-sm font-bold shadow-lg shadow-primary/20 hover:bg-primary/90 transition-all">
            Sign Up
          </button>
        </div>
      </div>
    </header>
  )
}

export default UserLogedOutNavbar
