import * as SocketIO from 'socket.io-client';

export const socket = SocketIO.connect();

export { socket as default };