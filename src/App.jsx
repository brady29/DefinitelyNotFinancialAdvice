import './App.css'
import * as React from 'react';
import TruthTable from './TruthTable.jsx'
import Nav from './Nav.jsx'
import StockBar from './stockBar.jsx';
import StockView from './StockView.jsx';
import Profile from './Profile.jsx';

export default function App(props) {

  // Which truth table are we showing? (main one or stock specific)
  const [currentDisplay, updateDisplay] = React.useState("main");

  // Which menu are we showing? (home or profile)
  const [menu, updateMenu] = React.useState("home");
  
  return (
    <>
      <div className='mainApp'>
        <Nav menu={menu} updateMenu={updateMenu} />
        <Profile menu={menu} />
        <StockBar currentDisplay={currentDisplay} updateDisplay={updateDisplay} menu={menu} />
        <TruthTable truths={props.truths} currentDisplay={currentDisplay} menu={menu} />
        <StockView currentDisplay={currentDisplay} menu={menu} />
      </div>
    </>
  )
}
