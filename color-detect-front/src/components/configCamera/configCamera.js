import { Component } from "react";
import {
  PrincipalConfigCamera,
  Header,
  Titulo,
  Content,
  ContentLinha01,
  ContentLinha02,
  InputIp,
  ButtonBlue,
} from "./styles";
import Swal from "sweetalert2";

export default class ConfigCamera extends Component {
  constructor(props) {
    super(props);

    this.state = {
      ipCamera: "",
    };
  }

  updateIp = (ip) => {
    this.setState({
      ipCamera: ip,
    });
  }

  updateIpMask = (e) => {
    let ip = e.target.value;
    if (e.target.value.length <= 15) {
      ip = ip.replace(/(\d{3})(\d)/, "$1.$2");
      ip = ip.replace(/(\d{3})(\d)/, "$1.$2");
      ip = ip.replace(/(\d{3})(\d)/, "$1.$2");
      this.updateIp(ip);
    } else if (e.target.value.length > 15) {
      return;
    }
  }

  conectarCamera = (e) => {
    if (this.state.ipCamera === '') {
        Swal.fire({
            icon: 'error',
            title: "Não permitido!",
            text: "Necessário informar Ip."
        })

        return;
    } else if (this.state.ipCamera.length < 15) {
        Swal.fire({
            icon: 'error',
            title: 'Não permitido!',
            text: 'Ip incorreto.'
        })
        
        return;
    }
    const ipArray = this.state.ipCamera.split(".");
    if (ipArray.length === 0) return;

    let ip0 = parseInt(ipArray[0]);
    let ip1 = parseInt(ipArray[1]);
    let ip2 = parseInt(ipArray[2]);
    let ip3 = parseInt(ipArray[3]);

    const url = `http://${ip0}.${ip1}.${ip2}.${ip3}:4000/cam01`;
    this.props.urlCamera(url);
  }

  render() {
    return (
      <PrincipalConfigCamera>
        <Header>
          <Titulo>Configurações Câmera</Titulo>
        </Header>
        <Content>
          <ContentLinha01>
            IP:
            <InputIp
              value={this.state.ipCamera}
              onChange={this.updateIpMask}
              placeholder="000.000.000.000"
            />
          </ContentLinha01>
          <ContentLinha02>
            <ButtonBlue onClick={this.conectarCamera}>Conectar</ButtonBlue>
          </ContentLinha02>
        </Content>
      </PrincipalConfigCamera>
    );
  }
}
