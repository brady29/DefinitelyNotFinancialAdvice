import './App.css'
import TruthTable from './TruthTable.jsx'
import Nav from './Nav.jsx'

export default function App(truths) {
  
  return (
    <>
      <div className='mainApp'>
        <Nav />
        <TruthTable truths={truths} />
      </div>
    </>
  )
}
