import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/settings/account')({
  component: RouteComponent,
})

function RouteComponent() {
  return (
    <div className="max-w-200 mx-auto px-4 md:px-8 py-10">
      <div className="mb-10">
        <h1 className="text-white text-4xl font-black leading-tight tracking-tight mb-2">
          Account Settings
        </h1>
        <p className="text-text-muted text-lg">
          Manage your account credentials, connected services, and active
          sessions.
        </p>
      </div>
      <div className="space-y-8">
        <section className="bg-card-dark p-6 rounded-xl border border-gray-200 dark:border-border-dark space-y-6">
          <h2 className="text-white text-xl font-bold border-b border-border-dark pb-4">
            Contact Information
          </h2>
          <div className="space-y-4">
            <div className="flex flex-col gap-2">
              <label className="text-white text-sm font-semibold">
                Email Address
              </label>
              <div className="flex gap-3">
                <input
                  className="form-input flex-1 rounded-lg text-white bg-background-dark border-gray-200 dark:border-border-dark focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4 transition-all"
                  type="email"
                  value="alex.rivers@example.com"
                />
                <button className="px-4 py-2 bg-primary/10 text-primary text-sm font-bold rounded-lg border border-primary/20 hover:bg-primary/20 transition-all">
                  Update
                </button>
              </div>
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-white text-sm font-semibold">
                Phone Number
              </label>
              <div className="flex gap-3">
                <input
                  className="form-input flex-1 rounded-lg text-white bg-background-dark border-gray-200 dark:border-border-dark focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4 transition-all"
                  type="tel"
                  value="+1 (555) 000-0000"
                />
                <button className="px-4 py-2 bg-primary/10 text-primary text-sm font-bold rounded-lg border border-primary/20 hover:bg-primary/20 transition-all">
                  Update
                </button>
              </div>
            </div>
          </div>
        </section>
        <section className="bg-card-dark p-6 rounded-xl border border-gray-200 dark:border-border-dark">
          <h2 className="text-white text-xl font-bold border-b border-border-dark pb-4 mb-6">
            Linked Accounts
          </h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-background-dark rounded-lg border border-gray-200 dark:border-border-dark">
              <div className="flex items-center gap-4">
                <div className="size-10 bg-white rounded-full flex items-center justify-center shadow-sm">
                  <svg className="size-6" viewBox="0 0 24 24">
                    <path
                      d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                      fill="#4285F4"
                    ></path>
                    <path
                      d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                      fill="#34A853"
                    ></path>
                    <path
                      d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"
                      fill="#FBBC05"
                    ></path>
                    <path
                      d="M12 5.38c1.62 0 3.06.56 4.21 1.66l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                      fill="#EA4335"
                    ></path>
                  </svg>
                </div>
                <div>
                  <p className="text-white font-bold">Google</p>
                  <p className="text-text-muted text-xs">
                    Connected as alex.rivers@gmail.com
                  </p>
                </div>
              </div>
              <button className="text-text-muted hover:text-white text-sm font-bold px-4 py-2 rounded-lg border border-border-dark hover:bg-card-dark transition-all">
                Disconnect
              </button>
            </div>
            <div className="flex items-center justify-between p-4 bg-background-dark rounded-lg border border-gray-200 dark:border-border-dark">
              <div className="flex items-center gap-4">
                <div className="size-10 bg-black rounded-full flex items-center justify-center text-white font-black text-xs">
                  42
                </div>
                <div>
                  <p className="text-white font-bold">42 School</p>
                  <p className="text-text-muted text-xs">Not connected</p>
                </div>
              </div>
              <button className="text-white bg-primary hover:bg-primary/90 text-sm font-bold px-4 py-2 rounded-lg transition-all">
                Connect
              </button>
            </div>
          </div>
        </section>
        <section className="bg-card-dark p-6 rounded-xl border border-gray-200 dark:border-border-dark">
          <div className="flex items-center justify-between border-b border-border-dark pb-4 mb-6">
            <h2 className="text-white text-xl font-bold">Active Sessions</h2>
            <button className="text-primary hover:underline text-sm font-bold">
              Log out everywhere
            </button>
          </div>
          <div className="space-y-4">
            <div className="flex items-center justify-between py-3">
              <div className="flex items-center gap-4">
                <span className="material-symbols-outlined text-text-muted text-3xl">
                  laptop_mac
                </span>
                <div>
                  <p className="text-white font-bold">MacBook Pro - Safari</p>
                  <p className="text-text-muted text-xs">
                    Paris, France • Current session
                  </p>
                </div>
              </div>
              <div className="px-2 py-1 rounded bg-green-500/10 text-green-500 text-[10px] font-bold uppercase tracking-wider border border-green-500/20">
                Active
              </div>
            </div>
            <div className="flex items-center justify-between py-3 border-t border-border-dark">
              <div className="flex items-center gap-4">
                <span className="material-symbols-outlined text-text-muted text-3xl">
                  smartphone
                </span>
                <div>
                  <p className="text-white font-bold">iPhone 15 - App</p>
                  <p className="text-text-muted text-xs">
                    Lyon, France • 2 hours ago
                  </p>
                </div>
              </div>
              <button className="text-text-muted hover:text-primary transition-colors">
                <span className="material-symbols-outlined">logout</span>
              </button>
            </div>
          </div>
        </section>
        <section className="bg-red-500/5 p-6 rounded-xl border border-red-500/20">
          <div className="flex items-start justify-between">
            <div className="space-y-1">
              <h2 className="text-red-500 text-lg font-bold">Delete Account</h2>
              <p className="text-text-muted text-sm max-w-md">
                Once you delete your account, there is no going back. All your
                history, watchlists, and profile data will be permanently
                removed.
              </p>
            </div>
            <button className="px-6 py-2 bg-red-500/10 hover:bg-red-500 text-red-500 hover:text-white border border-red-500/30 text-sm font-bold rounded-lg transition-all">
              Delete Account
            </button>
          </div>
        </section>
        <div className="flex items-center justify-end gap-4 border-t border-gray-200 dark:border-border-dark pt-8 pb-10">
          <button className="px-8 py-3 bg-transparent hover:hover:bg-card-dark text-text-muted hover:text-white text-base font-bold rounded-lg transition-all">
            Cancel
          </button>
          <button className="px-10 py-3 bg-primary hover:bg-primary/90 text-white text-base font-extrabold rounded-lg shadow-xl shadow-primary/20 transition-all">
            Save Changes
          </button>
        </div>
      </div>
    </div>
  )
}
