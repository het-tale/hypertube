import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/settings/billing')({
  component: RouteComponent,
})

function RouteComponent() {
  return (
    <div className="max-w-250 mx-auto px-4 md:px-8 py-10">
      <div className="mb-10">
        <h1 className="text-white text-4xl font-black leading-tight tracking-tight mb-2">
          Billing &amp; Subscription
        </h1>
        <p className="text-text-muted text-lg">
          Manage your plan, payment methods, and view your billing history.
        </p>
      </div>
      <div className="space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <section className="bg-card-dark p-6 rounded-xl border border-border-dark flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold uppercase tracking-widest text-text-muted">
                  Current Plan
                </span>
                <span className="px-2 py-1 bg-primary/10 text-primary text-[10px] font-bold rounded uppercase">
                  Active
                </span>
              </div>
              <h3 className="text-white text-2xl font-black mb-1">
                Premium 4K + HDR
              </h3>
              <p className="text-text-muted text-sm mb-4">
                Ultimate viewing experience with UHD and spatial audio.
              </p>
              <div className="flex items-baseline gap-1 mb-6">
                <span className="text-white text-3xl font-bold">$19.99</span>
                <span className="text-text-muted">/month</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-text-muted mb-6">
                <span className="material-symbols-outlined text-sm">
                  calendar_today
                </span>
                Next billing date:{' '}
                <span className="text-white font-medium">October 12, 2024</span>
              </div>
            </div>
            <button className="w-full py-3 bg-primary hover:bg-primary/90 text-white text-sm font-bold rounded-lg transition-all shadow-lg shadow-primary/20">
              Upgrade Plan
            </button>
          </section>
          <section className="bg-card-dark p-6 rounded-xl border border-border-dark flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold uppercase tracking-widest text-text-muted">
                  Payment Method
                </span>
                <button className="text-primary text-xs font-bold hover:underline">
                  Edit
                </button>
              </div>
              <div className="flex items-center gap-4 mb-6 p-4 bg-background-dark/50 rounded-lg border border-border-dark">
                <div className="size-12 bg-white/5 rounded flex items-center justify-center">
                  <span className="material-symbols-outlined text-white text-3xl">
                    credit_card
                  </span>
                </div>
                <div>
                  <p className="text-white font-bold">Visa ending in 4242</p>
                  <p className="text-text-muted text-xs uppercase tracking-wider">
                    Expires 12/26
                  </p>
                </div>
              </div>
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-text-muted">Email address</span>
                  <span className="text-white">alex.rivers@example.com</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-text-muted">Billing address</span>
                  <span className="text-white">United States</span>
                </div>
              </div>
            </div>
            <button className="w-full py-3 bg-transparent hover:bg-border-dark  text-white text-sm font-bold rounded-lg transition-all border border-gray-300 dark:border-border-dark mt-6">
              Update Payment Details
            </button>
          </section>
        </div>
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-white text-xl font-bold">Billing History</h3>
            <button className="text-text-muted hover:text-white text-sm flex items-center gap-2 transition-colors">
              <span className="material-symbols-outlined text-lg">
                download_for_offline
              </span>
              Download All (ZIP)
            </button>
          </div>
          <div className="overflow-hidden rounded-xl border border-border-dark">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-card-dark text-text-muted text-xs font-bold uppercase tracking-widest">
                  <th className="px-6 py-4 border-b border-border-dark">
                    Date
                  </th>
                  <th className="px-6 py-4 border-b border-border-dark">
                    Description
                  </th>
                  <th className="px-6 py-4 border-b border-border-dark">
                    Amount
                  </th>
                  <th className="px-6 py-4 border-b border-border-dark">
                    Status
                  </th>
                  <th className="px-6 py-4 border-b border-border-dark text-right">
                    Invoice
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-border-dark">
                <tr className="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors group">
                  <td className="px-6 py-4 text-sm text-white">Sep 12, 2023</td>
                  <td className="px-6 py-4 text-sm text-text-muted font-medium group-hover:text-white transition-colors">
                    Premium Subscription - Monthly
                  </td>
                  <td className="px-6 py-4 text-sm text-white font-bold">
                    $19.99
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-green-500/10 text-green-500 uppercase tracking-tighter">
                      Paid
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-text-muted hover:text-primary transition-colors">
                      <span className="material-symbols-outlined text-xl">
                        picture_as_pdf
                      </span>
                    </button>
                  </td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors group">
                  <td className="px-6 py-4 text-sm text-white">Aug 12, 2023</td>
                  <td className="px-6 py-4 text-sm text-text-muted font-medium group-hover:text-white transition-colors">
                    Premium Subscription - Monthly
                  </td>
                  <td className="px-6 py-4 text-sm text-white font-bold">
                    $19.99
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-green-500/10 text-green-500 uppercase tracking-tighter">
                      Paid
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-text-muted hover:text-primary transition-colors">
                      <span className="material-symbols-outlined text-xl">
                        picture_as_pdf
                      </span>
                    </button>
                  </td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors group">
                  <td className="px-6 py-4 text-sm text-white">Jul 12, 2023</td>
                  <td className="px-6 py-4 text-sm text-text-muted font-medium group-hover:text-white transition-colors">
                    Premium Subscription - Monthly
                  </td>
                  <td className="px-6 py-4 text-sm text-white font-bold">
                    $19.99
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-green-500/10 text-green-500 uppercase tracking-tighter">
                      Paid
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-text-muted hover:text-primary transition-colors">
                      <span className="material-symbols-outlined text-xl">
                        picture_as_pdf
                      </span>
                    </button>
                  </td>
                </tr>
                <tr className="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors group">
                  <td className="px-6 py-4 text-sm text-white">Jun 12, 2023</td>
                  <td className="px-6 py-4 text-sm text-text-muted font-medium group-hover:text-white transition-colors">
                    Premium Subscription - Monthly
                  </td>
                  <td className="px-6 py-4 text-sm text-white font-bold">
                    $19.99
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-green-500/10 text-green-500 uppercase tracking-tighter">
                      Paid
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-text-muted hover:text-primary transition-colors">
                      <span className="material-symbols-outlined text-xl">
                        picture_as_pdf
                      </span>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
        <div className="pt-6 border-t border-border-dark flex items-center justify-between">
          <div>
            <h4 className="text-white font-bold">Cancel Subscription</h4>
            <p className="text-text-muted text-sm">
              Once you cancel, you will still have access until the end of your
              billing cycle.
            </p>
          </div>
          <button className="px-6 py-2 text-primary border border-primary/20 hover:bg-primary/10 text-sm font-bold rounded-lg transition-all">
            Cancel Plan
          </button>
        </div>
      </div>
    </div>
  )
}
