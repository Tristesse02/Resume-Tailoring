import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import ResumeForm from './ResumeForm.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ResumeForm />
  </StrictMode>,
)
