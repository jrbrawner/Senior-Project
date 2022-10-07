import { configureStore } from '@reduxjs/toolkit'
import userReducer from './userSlice';

export default configureStore({
  reducer: {
    user: userReducer,
  },
})




/*import { createStore } from 'redux';


const initialState = {
    loggedIn: false,
    name: undefined
}

const reducer = (state = initialState, action) => {

    if (action.type === 'SET_LOGGED_IN'){
        return Object.assign({}, state, {
            loggedIn: state.loggedIn.concat(action.payload)
        })
    }

    if (action.type === 'SET_NAME'){
        return Object.assign({}, state, {
            name: state.name.concat(action.payload)
        })
    }

    return state
}


const store = createStore(reducer);

export default store

*/