import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/settings/notifications')({
  component: RouteComponent,
})

function RouteComponent() {
  return (
    <div className="max-w-200 mx-auto px-4 md:px-8 py-10">
      <div className="mb-10">
        <h1 className="text-white text-4xl font-black leading-tight tracking-tight mb-2">
          Notification Preferences
        </h1>
        <p className="text-text-muted text-lg">
          Choose how you want to be notified about your favorite content and
          account activity.
        </p>
      </div>
      <div className="space-y-8">
        <section className="space-y-4">
          <h3 className="text-white text-xl font-bold mb-4 flex items-center gap-2">
            <span className="material-symbols-outlined text-primary">
              campaign
            </span>
            Notification Channels
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-card-dark p-6 rounded-xl border border-border-dark flex flex-col items-center text-center gap-3">
              <span className="material-symbols-outlined text-3xl text-primary">
                mail
              </span>
              <div>
                <p className="text-white font-bold">Email</p>
                <p className="text-text-muted text-xs">For weekly summaries</p>
              </div>
              <label className="switch mt-2">
                <input checked={true} type="checkbox" />
                <span className="slider"></span>
              </label>
            </div>
            <div className="bg-card-dark p-6 rounded-xl border border-border-dark flex flex-col items-center text-center gap-3">
              <span className="material-symbols-outlined text-3xl text-primary">
                notifications_active
              </span>
              <div>
                <p className="text-white font-bold">Push</p>
                <p className="text-text-muted text-xs">For instant alerts</p>
              </div>
              <label className="switch mt-2">
                <input checked={true} type="checkbox" />
                <span className="slider"></span>
              </label>
            </div>
            <div className="bg-card-dark p-6 rounded-xl border border-border-dark flex flex-col items-center text-center gap-3">
              <span className="material-symbols-outlined text-3xl text-primary">
                sms
              </span>
              <div>
                <p className="text-white font-bold">SMS</p>
                <p className="text-text-muted text-xs">For security only</p>
              </div>
              <label className="switch mt-2">
                <input checked={false} type="checkbox" />
                <span className="slider"></span>
              </label>
            </div>
          </div>
        </section>
        <section className="space-y-4">
          <h3 className="text-white text-xl font-bold mb-4">
            Activity Categories
          </h3>
          <div className="bg-card-dark rounded-xl border border-border-dark divide-y divide-gray-200 dark:divide-border-dark">
            <div className="p-6 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="size-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                  <span className="material-symbols-outlined">movie</span>
                </div>
                <div>
                  <h4 className="text-white font-bold">New Movie Releases</h4>
                  <p className="text-text-muted text-sm">
                    Be the first to know when blockbuster movies land.
                  </p>
                </div>
              </div>
              <label className="switch">
                <input checked={true} type="checkbox" />
                <span className="slider"></span>
              </label>
            </div>
            <div className="p-6 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="size-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                  <span className="material-symbols-outlined">security</span>
                </div>
                <div>
                  <h4 className="text-white font-bold">
                    Account Security Alerts
                  </h4>
                  <p className="text-text-muted text-sm">
                    Notifications about login attempts and password changes.
                  </p>
                </div>
              </div>
              <label className="switch">
                <input checked={true} type="checkbox" />
                <span className="slider"></span>
              </label>
            </div>
            <div className="p-6 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="size-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                  <span className="material-symbols-outlined">update</span>
                </div>
                <div>
                  <h4 className="text-white font-bold">Product Updates</h4>
                  <p className="text-text-muted text-sm">
                    New features, improvements, and site maintenance.
                  </p>
                </div>
              </div>
              <label className="switch">
                <input checked={false} type="checkbox" />
                <span className="slider"></span>
              </label>
            </div>
            <div className="p-6 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="size-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                  <span className="material-symbols-outlined">recommend</span>
                </div>
                <div>
                  <h4 className="text-white font-bold">
                    Personalized Recommendations
                  </h4>
                  <p className="text-text-muted text-sm">
                    Content we think you'll love based on your history.
                  </p>
                </div>
              </div>
              <label className="switch">
                <input checked={true} type="checkbox" />
                <span className="slider"></span>
              </label>
            </div>
          </div>
        </section>
        <section className="bg-card-dark p-6 rounded-xl border border-border-dark">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className="size-10 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-500">
                <span className="material-symbols-outlined">
                  notifications_paused
                </span>
              </div>
              <div>
                <h4 className="text-white font-bold">Quiet Mode</h4>
                <p className="text-text-muted text-sm">
                  Silence notifications during specific hours.
                </p>
              </div>
            </div>
            <label className="switch">
              <input checked={true} type="checkbox" />
              <span className="slider"></span>
            </label>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div className="flex flex-col gap-2">
              <label className="text-white text-xs font-bold uppercase tracking-wider">
                Start Time
              </label>
              <input
                className="form-input w-full rounded-lg text-white bg-border-dark border-border-dark focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4 transition-all"
                type="time"
                value="22:00"
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-white text-xs font-bold uppercase tracking-wider">
                End Time
              </label>
              <input
                className="form-input w-full rounded-lg text-white bg-border-dark border-border-dark focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4 transition-all"
                type="time"
                value="08:00"
              />
            </div>
          </div>
        </section>
        <div className="flex items-center justify-between border-t border-border-dark pt-8 pb-10">
          <button className="px-8 py-3 bg-transparent hover:bg-gray-100 dark:hover:bg-card-dark text-text-muted hover:text-white text-base font-bold rounded-lg transition-all">
            Discard Changes
          </button>
          <button className="px-10 py-3 bg-primary hover:bg-primary/90 text-white text-base font-extrabold rounded-lg shadow-xl shadow-primary/20 transition-all hover:-translate-y-0.5 active:translate-y-0">
            Save Preferences
          </button>
        </div>
      </div>
    </div>
  )
}
