import { 
  createBrowserRouter, 
  createRoutesFromElements, 
  Route, 
  RouterProvider 
} from 'react-router-dom'

// layouts and pages
import  RootLayout  from './layouts/RootLayout';
import Dashboard, { tasksLoader } from './pages/Dashboard'
import Home from './pages/Home'
import Contact from './pages/Contact';
import ReactGA from "react-ga4";

// router and routes
const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<RootLayout />}>
      <Route index element={<Home />} />
      <Route path="dashboard" element={<Dashboard />} loader={tasksLoader} />
      <Route path="contact" element={<Contact />} />
    </Route>
  )
)

function App() {
  if (process.env.NODE_ENV === "production") {
    ReactGA.initialize("G-QMRN96PC4B");
    ReactGA.send({ hitType: "pageview", page: "/", title: "App" });
  }
  return (
    <RouterProvider router={router} />
  )
}

export default App
