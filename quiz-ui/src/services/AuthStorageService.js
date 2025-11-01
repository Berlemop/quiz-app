export default {
  saveToken(token) {
    window.localStorage.setItem("authToken", token);
  },
  getToken() {
    return window.localStorage.getItem("authToken");
  },
  clearToken() {
    window.localStorage.removeItem("authToken");
  }
};
