import Body from '../components/Body'
import Providers from '../components/ProviderComponents/Providers'

import React from 'react';
import ReactDOM from 'react-dom';

//testing imports only after this point
import { useState } from 'react';

export default function ProvidersPage(){
    
  function myFunction() {
    return( <p>Fubar</p>);
  }

  function mySecondFunction(){
    return(
    <Body sidebar>
      <Providers /> 
    </Body>
    );
  }

  function myThirdFunction(){ //this is an example of flex positioning 
    return(
        <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        }}>
        Hello world
        </div>

    );
  }

  function topButton1(){
    return(
      //<fragment style={{display:'inline-block'}}>
        <button type="button" style={{display:'inline-block'}}> Organizations </button>
      //</fragment>
    );
  }

  function topButton2(){
    return(
      //<fragment>
        <button type="button" style={{display:'inline-block'}}> Locations </button>
      //</fragment>
    );
  }

  function topButton3(){
    return(
      <button type="button" style={{display:'inline-block'}}> People </button>
    );
  }

  function topButton4(){
    return(
      <button type="button" style={{display:'inline-block'}}> Messages </button>
    );
  }

  function topSearch(){
    return(
      <fragment style={{display:'inline-block'}}> Search Bar Here </fragment>
    );
  }

  function topButton5(){
    return(
      <button type="button" style={{display:'inline-block'}}> Notifications </button>
    );
  }

  function topButton6(){
    return(
      <button type="button" style={{display:'inline-block'}}> Profile </button>
    );
  }
    

  function secondTopButton1(){
    return(
      <button type="button" style={{display:'inline-block'}}> Create New Organization </button>
    );
  }

    return[ //make sure you use the bracket things instead of the () because apparently there was an html update that makes that not compatible with what we are doing here

        //seperate all functions with a comma, no simicolons
        //in the order that you want them called on the display
        //so this means left to right and up to down

        /*myFunction(),      
        myThirdFunction(),
        mySecondFunction()*/
    //examples end


        topButton1(),
        topButton2(),
        topButton3(),
        topButton4(),
        topSearch(),
        topButton5(),
        secondTopButton1()

    ];
}




/* export default */ /*function MyForm() {
    const [inputs, setInputs] = useState({});
  
    const handleChange = (event) => {
      const name = event.target.name;
      const value = event.target.value;
      setInputs(values => ({...values, [name]: value}))
    }
  
    const handleSubmit = (event) => {
      event.preventDefault();
      alert(inputs);
    }
  
    
    return (
      <form onSubmit={handleSubmit}>
        <label>Provider ID
        <input
            type="text"
            name="username"
            value={inputs.userid || "1"}
            onChange={handleChange}
        />
        </label>
        <label>Provider Name:
        <input 
            type="text" 
            name="username" 
            value={inputs.username || "hello"} 
            onChange={handleChange}
        />
        </label>
        <label>Twillio Account ID
        <input
            type="text"
            name="username"
            value={inputs.userid || "###-###-#####"}
            onChange={handleChange}
        />
        </label>
        <label>Provider contact number:
          <input 
            type="number" 
            name="age" 
            value={inputs.age || "8128128121"} 
            onChange={handleChange}
          />
          </label>
          <input type="submit" />
      </form>
      
      
    )
  }

//testing values
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<MyForm />);



//testing values end

*/
