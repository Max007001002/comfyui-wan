import { ChakraProvider } from '@chakra-ui/react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <ChakraProvider>
      <Router>
        <Routes>
          <Route path="/" element={<div>Welcome to WAN I2V</div>} />
        </Routes>
      </Router>
    </ChakraProvider>
  )
}

export default App 