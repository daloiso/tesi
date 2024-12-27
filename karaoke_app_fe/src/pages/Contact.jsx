import ReactGA from "react-ga4";

const Contact = () => {
  if (process.env.NODE_ENV === "production") {
    ReactGA.send({ hitType: "pageview", page: "/contact", title: "Contact" });
  }
  return (
    <div>Contattami via e-mail all'indirizzo di posta elettronica pasquale.daloiso@gmail.com</div>
  )
}
export default Contact;