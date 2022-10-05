import { createSlice } from '@reduxjs/toolkit'

export const userSlice = createSlice({
  name: 'user',
  initialState: {
    name: "",
    loggedIn: false,

  },
  reducers: {
    setName: (state, action) => {
      // Redux Toolkit allows us to write "mutating" logic in reducers. It
      // doesn't actually mutate the state because it uses the Immer library,
      // which detects changes to a "draft state" and produces a brand new
      // immutable state based off those changes
      state.name = action.payload
    },
    setLoggedIn: (state, action) => {
      state.loggedIn = action.payload
    },

    
  },
})

// Action creators are generated for each case reducer function
export const { setName, setLoggedIn } = userSlice.actions

export default userSlice.reducer