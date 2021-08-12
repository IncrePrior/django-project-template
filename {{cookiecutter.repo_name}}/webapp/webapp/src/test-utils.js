/* eslint-disable import/no-extraneous-dependencies */
import React from 'react';
import { render as rtlRender } from '@testing-library/react';
import { Provider } from 'react-redux';

import createAppStore from './store';

function render(ui, { store = createAppStore({}), ...renderOptions } = {}) {
    // eslint-disable-next-line react/prop-types
    function Wrapper({ children }) {
        return <Provider store={store}>{children}</Provider>;
    }
    return rtlRender(ui, { wrapper: Wrapper, ...renderOptions });
}

// re-export everything
export * from '@testing-library/react';

// override render method
export { render };
