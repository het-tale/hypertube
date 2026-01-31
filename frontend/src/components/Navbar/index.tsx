import { useState, Activity } from 'react'
import UserLoggedOutNavbar from './userLogOut'
import UserLoggedInNavbar from './userLogedIn'
export default function Header() {
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(true)
  const login = () => {
    setIsUserLoggedIn(true)
  }
  const logout = () => {
    console.log('logout')
    setIsUserLoggedIn(false)
  }

  return (
    <>
      <Activity mode={isUserLoggedIn ? 'hidden' : 'visible'}>
        <UserLoggedOutNavbar login={login} />
      </Activity>
      <Activity mode={isUserLoggedIn ? 'visible' : 'hidden'}>
        <UserLoggedInNavbar logout={logout} />
      </Activity>
    </>
  )
}
