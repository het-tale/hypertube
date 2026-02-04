import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/settings/security')({
  component: RouteComponent,
})

function RouteComponent() {
  return (
    <div className="max-w-200 mx-auto px-4 md:px-8 py-10">
      <div className="mb-10">
        <h1 className="text-white text-4xl font-black leading-tight tracking-tight mb-2">
          Security &amp; Privacy
        </h1>
        <p className="text-text-muted text-lg">
          Control your account security and monitor access activity.
        </p>
      </div>
      <div className="space-y-8">
        <section className="bg-card-dark p-6 rounded-xl border border-gray-200 dark:border-border-dark">
          <div className="flex items-center gap-3 mb-6">
            <span className="material-symbols-outlined text-primary">lock</span>
            <h3 className="text-white text-xl font-bold">Change Password</h3>
          </div>
          <div className="space-y-4">
            <div className="flex flex-col gap-2">
              <label className="text-white text-sm font-semibold">
                Current Password
              </label>
              <input
                className="form-input w-full rounded-lg text-white bg-background-dark border-gray-200 dark:border-border-dark focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4 transition-all"
                placeholder="••••••••"
                type="password"
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex flex-col gap-2">
                <label className="text-white text-sm font-semibold">
                  New Password
                </label>
                <input
                  className="form-input w-full rounded-lg text-white bg-background-dark border-gray-200 dark:border-border-dark focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4 transition-all"
                  placeholder="••••••••"
                  type="password"
                />
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-white text-sm font-semibold">
                  Confirm New Password
                </label>
                <input
                  className="form-input w-full rounded-lg text-white bg-background-dark border-gray-200 dark:border-border-dark focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4 transition-all"
                  placeholder="••••••••"
                  type="password"
                />
              </div>
            </div>
            <div className="pt-2">
              <button className="px-6 py-2.5 bg-primary hover:bg-primary/90 text-white text-sm font-bold rounded-lg transition-all">
                Update Password
              </button>
            </div>
          </div>
        </section>
        <section className="bg-card-dark p-6 rounded-xl border border-gray-200 dark:border-border-dark">
          <div className="flex items-start justify-between">
            <div className="flex gap-4">
              <div className="size-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                <span className="material-symbols-outlined">verified_user</span>
              </div>
              <div>
                <h3 className="text-white text-lg font-bold mb-1">
                  Two-Factor Authentication (2FA)
                </h3>
                <p className="text-text-muted text-sm max-w-md">
                  Add an extra layer of security to your account. We'll ask for
                  a code whenever you log in on a new device.
                </p>
              </div>
            </div>
            <div className="relative inline-block w-12 h-6 align-middle select-none transition duration-200 ease-in">
              <input
                checked={true}
                className="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 border-transparent appearance-none cursor-pointer z-10 transition-transform duration-200 ease-in translate-x-0"
                id="toggle"
                name="toggle"
                type="checkbox"
              />
              <label
                className="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 dark:bg-border-dark cursor-pointer transition-colors duration-200 ease-in"
                htmlFor="toggle"
              ></label>
              <span className="toggle-dot absolute left-0 top-0 bg-white w-6 h-6 rounded-full border-4 border-transparent transition-transform duration-200 ease-in"></span>
            </div>
          </div>
        </section>
        <section className="bg-card-dark rounded-xl border border-gray-200 dark:border-border-dark overflow-hidden">
          <div className="p-6 border-b border-gray-200 dark:border-border-dark">
            <h3 className="text-white text-xl font-bold">Login History</h3>
            <p className="text-text-muted text-sm">
              Recent activity from your devices and browsers.
            </p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead className="bg-background-dark/50">
                <tr>
                  <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-text-muted">
                    Device / Browser
                  </th>
                  <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-text-muted">
                    IP Address
                  </th>
                  <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-text-muted">
                    Location
                  </th>
                  <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-text-muted text-right">
                    Time
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-border-dark">
                <tr>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <span className="material-symbols-outlined text-text-muted">
                        desktop_windows
                      </span>
                      <div>
                        <p className="text-sm font-semibold text-white">
                          Chrome on macOS
                        </p>
                        <p className="text-xs text-green-500 font-medium">
                          Current Session
                        </p>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-text-muted">
                    192.168.1.45
                  </td>
                  <td className="px-6 py-4 text-sm text-text-muted">
                    Paris, France
                  </td>
                  <td className="px-6 py-4 text-sm text-text-muted text-right">
                    Just now
                  </td>
                </tr>
                <tr>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <span className="material-symbols-outlined text-text-muted">
                        smartphone
                      </span>
                      <div>
                        <p className="text-sm font-semibold text-white">
                          iPhone 14 Pro
                        </p>
                        <p className="text-xs text-text-muted">Hypertube App</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-text-muted">
                    172.20.10.1
                  </td>
                  <td className="px-6 py-4 text-sm text-text-muted">
                    Lyon, France
                  </td>
                  <td className="px-6 py-4 text-sm text-text-muted text-right">
                    2 hours ago
                  </td>
                </tr>
                <tr>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <span className="material-symbols-outlined text-text-muted">
                        laptop
                      </span>
                      <div>
                        <p className="text-sm font-semibold text-white">
                          Safari on MacBook
                        </p>
                        <p className="text-xs text-text-muted">macOS Ventura</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-text-muted">
                    82.124.15.89
                  </td>
                  <td className="px-6 py-4 text-sm text-text-muted">
                    Berlin, Germany
                  </td>
                  <td className="px-6 py-4 text-sm text-text-muted text-right">
                    Oct 24, 2023
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
        <section className="bg-red-500/5 p-6 rounded-xl border border-red-500/20">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
            <div>
              <h3 className="text-red-500 text-lg font-bold">Delete Account</h3>
              <p className="text-text-muted text-sm">
                Once you delete your account, there is no going back. Please be
                certain.
              </p>
            </div>
            <button className="px-6 py-2.5 border border-red-500/50 hover:bg-red-500 text-red-500 hover:text-white text-sm font-bold rounded-lg transition-all">
              Delete My Account
            </button>
          </div>
        </section>
      </div>
    </div>
  )
}
