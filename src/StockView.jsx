import * as React from 'react';

export default function StockView(props) {
    return (
        <div id="stock" style={{display: (props.menu == "home" && props.currentDisplay != "main") ? '' : 'none'}}>
            <h1>{props.currentDisplay}</h1>
            <div className="truth">
            </div>
        </div>
    );
}