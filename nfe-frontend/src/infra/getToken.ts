export const getUserFromLocalStorage = () => {
  const getLocal = localStorage.getItem('erp')!;
  const getParse = JSON.parse(getLocal);
  return getParse;
};
