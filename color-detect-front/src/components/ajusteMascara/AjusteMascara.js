import { Component } from "react";
import {
  PrincipalAjusteMascara,
  Header,
  InputAjuste,
  Content,
  ContentLinha01,
  ContentLinha02,
  ContentLinha03,
  ContentLinha04,
  Titulo,
  ButtonBlue,
  ContentLinha05,
} from "./styles";
import axios from "axios";
import Swal from "sweetalert2";

export default class AjusteMascara extends Component {
  constructor(props) {
    super(props);

    this.state = {
      urlCamera: "",
      x1: 0,
      y1: 0,
      x2: 0,
      y2: 0,
      x3: 0,
      y3: 0,
      x4: 0,
      y4: 0,
    };
  }

  componentWillReceiveProps = async (props) => {
    this.setState({
      urlCamera: props.urlCamera,
    });

    await this.getMask();
  }

  updateIputs = (e) => {
    switch (e.target.name) {
      case "x1":
        this.setState({ x1: e.target.value });
        break;
      case "y1":
        this.setState({ y1: e.target.value });
        break;
      case "x2":
        this.setState({ x2: e.target.value });
        break;
      case "y2":
        this.setState({ y2: e.target.value });
        break;
      case "x3":
        this.setState({ x3: e.target.value });
        break;
      case "y3":
        this.setState({ y3: e.target.value });
        break;
      case "x4":
        this.setState({ x4: e.target.value });
        break;
      case "y4":
        this.setState({ y4: e.target.value });
        break;
      default:
        break;
    }
  }

  getMask = async () => {
    if (this.state.urlCamera === '') {
        return;
    }

    let ip0 = this.state.urlCamera.split(".")[0].replace("http://", "");
    let ip1 = this.state.urlCamera.split(".")[1];
    let ip2 = this.state.urlCamera.split(".")[2];
    let ip3 = this.state.urlCamera.split(".")[3];

    await axios
      .get(`http://${ip0}.${ip1}.${ip2}.${ip3}/mask`, { timeout: 3000 })
      .then((response) => {
        console.log(response.data);
        let data = response.data;
        if (data) {
          this.setState({
            x1: parseInt(data.mask['mask'][0]),
            y1: parseInt(data.mask['mask'][1]),
            x2: parseInt(data.mask['mask'][2]),
            y2: parseInt(data.mask['mask'][3]),
            x3: parseInt(data.mask['mask'][4]),
            y3: parseInt(data.mask['mask'][5]),
            x4: parseInt(data.mask['mask'][6]),
            y4: parseInt(data.mask['mask'][7]),
          });
        }
      })
      .catch((error) => {
        let message = "Ocorreu um erro ao buscar a máscara.\nTente novamente.";
        if (error.status === 400 || error.status === 500) {
          message = error.data.error;
        } else if (error.status === 404) {
          message = error.data.message;
        }
        Swal.fire({
          icon: "error",
          title: "Ops.",
          text: message,
        });
      });
  }

  saveMask = async () => {

    if (this.state.urlCamera === '') {
        Swal.fire({
            icon: 'error',
            title: 'Não permitido!',
            text: 'É necessário conectar-se à um controlador para realizar esta ação.'
        });

        return;
    }
    let x1 = this.state.x1;
    let y1 = this.state.y1;
    let x2 = this.state.x2;
    let y2 = this.state.y2;
    let x3 = this.state.x3;
    let y3 = this.state.y3;
    let x4 = this.state.x4;
    let y4 = this.state.y4;

    let mask = { mask: `${x1},${y1},${x2},${y2},${x3},${y3},${x4},${y4}` };

    let ip0 = this.state.urlCamera.split(".")[0].replace('http://', '')
    let ip1 = this.state.urlCamera.split(".")[1];
    let ip2 = this.state.urlCamera.split(".")[2];
    let ip3 = this.state.urlCamera.split(".")[3];

    await axios
      .post(`http://${ip0}.${ip1}.${ip2}.${ip3}/mask`, mask, { timeout: 3000 })
      .then((response) => {
        Swal.fire({
          icon: "success",
          title: "Salvo.",
          text: response.data.message,
        });
      })
      .catch((error) => {
        let message = "Ocorreu um erro ao salvar a máscara.\nTente novamente.";
        if (error.status === 400 || error.status === 500) {
          message = error.data.error;
        } else if (error.status === 404) {
          message = error.data.message;
        }
        Swal.fire({
          icon: "error",
          title: "Ops.",
          text: message,
        });
      });
  }

  render() {
    return (
      <PrincipalAjusteMascara>
        <Header>
          <Titulo>Ajuste Máscara</Titulo>
        </Header>
        <Content>
          <ContentLinha01>
            1x:
            <InputAjuste
              name="x1"
              type="number"
              value={this.state.x1}
              onChange={this.updateIputs}
            />
            1y:
            <InputAjuste
              name="y1"
              type="number"
              value={this.state.y1}
              onChange={this.updateIputs}
            />
          </ContentLinha01>
          <ContentLinha02>
            2x:
            <InputAjuste
              name="x2"
              type="number"
              value={this.state.x2}
              onChange={this.updateIputs}
            />
            2y:
            <InputAjuste
              name="y2"
              type="number"
              value={this.state.y2}
              onChange={this.updateIputs}
            />
          </ContentLinha02>
          <ContentLinha03>
            3x:
            <InputAjuste
              name="x3"
              type="number"
              value={this.state.x3}
              onChange={this.updateIputs}
            />
            3y:
            <InputAjuste
              name="y3"
              type="number"
              value={this.state.y3}
              onChange={this.updateIputs}
            />
          </ContentLinha03>
          <ContentLinha04>
            4x:
            <InputAjuste
              name="x4"
              type="number"
              value={this.state.x4}
              onChange={this.updateIputs}
            />
            4y:
            <InputAjuste
              name="y4"
              type="number"
              value={this.state.y4}
              onChange={this.updateIputs}
            />
          </ContentLinha04>
          <ContentLinha05>
            <ButtonBlue onClick={this.saveMask}>Atualizar Máscara</ButtonBlue>
          </ContentLinha05>
        </Content>
      </PrincipalAjusteMascara>
    );
  }
}
