import {
  Outlet,
  createRootRouteWithContext,
  redirect,
} from '@tanstack/react-router'
// import { TanStackRouterDevtoolsPanel } from '@tanstack/react-router-devtools'
// import { TanStackDevtools } from '@tanstack/react-devtools'

import Header from '../components/Navbar/index'

// import TanStackQueryDevtools from '../integrations/tanstack-query/devtools'

import { getLocale, shouldRedirect } from '@/paraglide/runtime'

import type { QueryClient } from '@tanstack/react-query'

interface MyRouterContext {
  queryClient: QueryClient
}

export const Route = createRootRouteWithContext<MyRouterContext>()({
  beforeLoad: async () => {
    // Other redirect strategies are possible; see
    // https://github.com/TanStack/router/tree/main/examples/react/i18n-paraglide#offline-redirect
    if (typeof document !== 'undefined') {
      document.documentElement.setAttribute('lang', getLocale())
    }

    // Client-side fallback redirect for SPA/file-router builds. Start apps should
    // prefer server-side paraglideMiddleware (see start template server.ts).
    if (typeof window !== 'undefined') {
      const decision = await shouldRedirect({ url: window.location.href })

      if (decision.redirectUrl) {
        throw redirect({ href: decision.redirectUrl.href })
      }
    }
  },

  component: () => (
    <div className="flex flex-col h-screen bg-background-light dark:bg-background-dark font-display text-white dark:text-white transition-colors duration-300 min-h-screen">
      <Header />
      <div className="flex-1 overflow-hidden">
        <Outlet />
      </div>
    </div>
  ),
})
