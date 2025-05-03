import './App.css'
import StockBar from './StockBar.jsx'
import TruthTable from './TruthTable.jsx'
import Nav from './Nav.jsx'

export default function App(truths) {
  
  return (
    <>
      <div className='mainApp'>
        <Nav />
        <StockBar />
        <TruthTable truths={truths} />
      </div>
    </>
  )
}
