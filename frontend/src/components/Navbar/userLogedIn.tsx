import { useMe } from '@/features/auth/hooks/useAuthQueries'
import { Link } from '@tanstack/react-router'

const UserLogedInNavbar = () => {
  const { data: user } = useMe() // TODO: get user data from context or hook

  console.log('Logged in user:', user)
  console.log('Logged in user:', user?.profile_picture)
  return (
    <header className="sticky top-0 z-50 glass-nav dark:border-border-dark px-6 lg:px-20 py-4">
      <div className="max-w-360 mx-auto flex items-center justify-between gap-8">
        <div className="flex items-center gap-10">
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
          <nav className="hidden md:flex items-center gap-8">
            <a
              className="text-white font-medium hover:text-primary transition-colors"
              href="#"
            >
              Movies
            </a>
            <a
              className="text-white/60 font-medium hover:text-white transition-colors"
              href="#"
            >
              TV Shows
            </a>
            <a
              className="text-white/60 font-medium hover:text-white transition-colors"
              href="#"
            >
              My List
            </a>
          </nav>
        </div>
        <div className="flex-1 max-w-md hidden sm:block">
          <div className="relative group">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-white/40 group-focus-within:text-primary">
              <span className="material-symbols-outlined text-xl!">search</span>
            </div>
            <input
              className="block w-full bg-white/5 border-none rounded-xl py-2.5 pl-10 pr-4 text-sm text-white placeholder-white/40 focus:ring-2 focus:ring-primary/50 transition-all"
              placeholder="Search for titles, actors, or genres..."
              type="text"
            />
          </div>
        </div>
        <div className="flex items-center gap-4">
          <button className="p-2.5 rounded-xl bg-white/5 text-white/70 hover:bg-white/10 hover:text-white transition-all relative">
            <span className="material-symbols-outlined">notifications</span>
            <span className="absolute top-2 right-2 w-2 h-2 bg-primary rounded-full border-2 border-background-dark"></span>
          </button>
          <Link
            to="/settings/profile"
            className="size-10 rounded-xl overflow-hidden cursor-pointer border border-white/10 hover:border-primary transition-all"
          >
            <img
              className="w-full h-full object-cover"
              referrerPolicy="no-referrer"
              data-alt="User profile avatar with red abstract accent"
              src={user?.profile_picture}
            />
          </Link>
        </div>
      </div>
    </header>
  )
}

export default UserLogedInNavbar
