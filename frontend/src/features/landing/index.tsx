import FeaturesSection from './components/featuresSection'
import Hero from './components/hero'
import TrendingMovies from './components/trending'

const LandingPage = () => {
  return (
    <div className="flex flex-col ">
      <Hero />
      <FeaturesSection />
      <TrendingMovies />
    </div>
  )
}

export default LandingPage
