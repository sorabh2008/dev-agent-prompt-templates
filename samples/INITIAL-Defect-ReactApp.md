# INITIAL.md – Defect: Cart Item Count Not Updating

## Problem
Cart icon badge does not update after adding an item.

## Observed Behavior
Badge shows old count until page refresh.

## Expected Behavior
Badge updates immediately after adding item.

## Paths to Inspect
- `/src/components/CartIcon.tsx`
- `/src/state/cartReducer.ts`
- `/src/state/selectors/cart.ts`

## Search Keywords
`updateCartCount`, `ADD_TO_CART`, `useSelector`, `memo`, `CartIcon`

## Hypotheses
- Selector memoization misses dependency
- Reducer not returning new reference
- Component wrapped in React.memo without prop change

## Done When
- Badge updates on add/remove events
- Unit tests added for reducer + selector
- RTL test verifies badge after clicking "Add to cart"