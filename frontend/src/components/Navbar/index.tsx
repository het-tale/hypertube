import UserLoggedOutNavbar from './userLogOut'
import { useMatches } from '@tanstack/react-router'
import UserLoggedInNavbar from './userLogedIn'
import { useAuth } from '@/features/auth/hooks/useAuth'
export default function Header() {
  const { isAuthenticated, isLoading } = useAuth()
  const matches = useMatches()
  const currentPath = matches[matches.length - 1]?.pathname

  // Routes where we DON'T want to show the header
  const noHeaderRoutes = ['/SignIn', '/Signup']
  const shouldShowHeader = !noHeaderRoutes.includes(currentPath)

  if (!isLoading && !shouldShowHeader) {
    return null // or a loading spinner
  }
  return isAuthenticated ? <UserLoggedInNavbar /> : <UserLoggedOutNavbar />
}
