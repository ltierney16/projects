import { useState, useEffect } from 'react' // import useState to allow us to set variables with a build in function
import './App.css' // importing the CSS styling

// URL that can be set in /frontend/.env to be the URL of whatever server you are hosting the frontend on
const BASE_URL = import.meta.env.VITE_API_URL

// component that contains the whole calculator app that we are default exporting to main.jsx
export default function App() {

  const [display, setDisplay] = useState("") // variable to hold whatever will be displayed in the top box which could be the expression, result or an Error message if the calculation was not possible
  const [calculated, setCalculated] = useState(false) // variable to determine whether the calculate button has just been pressed or not
  const clearLabel = calculated ? "AC" : "CE" // variable that holds AC if calculated is true, else it holds CE
  const [logs, setLogs] = useState([]) // variable to hold the history of calculations
  const [historyIndex, setHistoryIndex] = useState(-1) // used to track the index in logs taht is being displayed, -1 means we are not browsing old calculations currently
  const [savedDisplay, setSavedDisplay] = useState("") // holds the live display while browsing history of calculations

  // fetch history once when the app first loads
  useEffect(() => {
    fetch(`${BASE_URL}/api/history`)
      .then(res => res.json())
      .then(data => setLogs(data))
      .catch(err => console.error('Could not fetch history:', err));
  }, []);

  //function to handle adding something to the display string
  const handleAppend = (buttonInput) => {
    if (historyIndex !== -1) {
      return;
    }
    if (display.toString().length >= 17) {
      return;
    }
    else {
      setCalculated(false);
      const char = display.toString().slice(-1);
      if (((["+", "-", "/", "*"].includes(char)) && (["+", "-", "/", "*"].includes(buttonInput))) || (char === "(" && buttonInput === ")")) {
        return;
      } else {
        setDisplay(display + buttonInput);
      }
    }
  }

  // function to handle deletes
  const handleDelete = () => {
    if (calculated) {
      setCalculated(false);
      setDisplay("");
      setHistoryIndex(-1);
    } else {
      setDisplay(display => display.toString().slice(0, -1));
    } 
  } 

  //function to handle calculates
  const handleCalculate = () => {
    if (historyIndex !== -1) {
      return;
    } else {
      const expr = display.toString();
      setCalculated(true);
      try {
        const result = new Function(`return (${expr})`)();
        if (typeof result === 'number' && !isNaN(result) && isFinite(result)) {
          setDisplay(result);

          //save this calculation to the backend/database
          fetch(`${BASE_URL}/api/history`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              expression: expr,
              result: result.toString()
            })
          })
          .then(res => {
            if (!res.ok) throw new Error('Failed to save calculation');
            return res.json();
          })
          .then(saved => {
            // add the newly saved calculation to our local history list too
            setLogs(prevLogs => [...prevLogs, saved]);
          })
          .catch(err => console.error('Could not save calculation:', err));

        } else {
          setDisplay('Error');
        }
      } catch {
        setDisplay('Error');
      }
    }

  };

  // moves to an older entry in history
  const handleUp = () => {

    // if there are no prior calculations
    if (logs.length === 0) return;

    // if we're just starting to browse, remember what was on the live display
    if (historyIndex === -1) {
      setSavedDisplay(display);
    }

    const nextIndex = historyIndex + 1;
    if (nextIndex < logs.length) {
      setHistoryIndex(nextIndex);
      const entry = logs[logs.length - 1 - nextIndex]; // newest-first navigation
      setDisplay(`${entry.expression} = ${entry.result}`);
      setCalculated(true);
    }
  }

  // moves to a newer entry in history or back to live display
  const handleDown = () => {
    if (historyIndex === -1) return; // already at the live display, nothing newer

    const nextIndex = historyIndex - 1;
    if (nextIndex === -1) {
      // back to the live display
      setHistoryIndex(-1);
      setDisplay(savedDisplay);
    } else {
      setHistoryIndex(nextIndex);
      const entry = logs[logs.length - 1 - nextIndex];
      setDisplay(`${entry.expression} = ${entry.result}`);
      setCalculated(true);
    }
  }

  // the structure of the root
  return (
    <div className="page">
      <div className="calculator">
        <div className="display-row">
          <div 
            className="display-box"
            style={{
              backgroundColor: historyIndex !== -1 ? '#1e293b' : undefined,
              transition: 'background-color 0.2s ease'
            }}
          >
            {display}
          </div>
          <div className="arrow-group">
            <button className="arrow" onClick={handleUp}>↑</button>
            <button className="arrow" onClick={handleDown}>↓</button>
          </div>
        </div>
        <div className="row">
          <button onClick={() => handleAppend('(')} className="nums">(</button>
          <button onClick={() => handleAppend(')')} className="nums">)</button>
          <button onClick={() => handleAppend('%')} className="nums">%</button>
          <button onClick={handleDelete} className="clearButton">{clearLabel}</button>
        </div>
        <div className="row">
          <button onClick={() => handleAppend('7')} className="nums">7</button>
          <button onClick={() => handleAppend('8')} className="nums">8</button>
          <button onClick={() => handleAppend('9')} className="nums">9</button>
          <button onClick={() => handleAppend('/')} className="op">/</button>
        </div>
        <div className="row">
          <button onClick={() => handleAppend('4')} className="nums">4</button>
          <button onClick={() => handleAppend('5')} className="nums">5</button>
          <button onClick={() => handleAppend('6')} className="nums">6</button>
          <button onClick={() => handleAppend('*')} className="op">*</button>
        </div>
        <div className="row">
          <button onClick={() => handleAppend('1')} className="nums">1</button>
          <button onClick={() => handleAppend('2')} className="nums">2</button>
          <button onClick={() => handleAppend('3')} className="nums">3</button>
          <button onClick={() => handleAppend('-')} className="op">-</button>
        </div>
        <div className="row">
          <button onClick={() => handleAppend('0')} className="nums">0</button>
          <button onClick={() => handleAppend('.')} className="nums">.</button>
          <button onClick={handleCalculate}>=</button>
          <button onClick={() => handleAppend('+')} className="op">+</button>
        </div>
      </div>
    </div>
  )
}