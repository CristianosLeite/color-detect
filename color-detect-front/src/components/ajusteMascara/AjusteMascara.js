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

  componentWillReceiveProps = (props) => {
    this.setState({
      urlCamera: props.urlCamera,
    });

    this.getMask();
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

  getMask = () => {
    axios
      .get(`http://127.0.0.1:4000/cam01/mask`, { timeout: 3000 })
      .then((response) => {
        let data = response.data;
        if (data) {
          this.setState({
            x1: parseInt(data.mask[0]),
            y1: parseInt(data.mask[1]),
            x2: parseInt(data.mask[2]),
            y2: parseInt(data.mask[3]),
            x3: parseInt(data.mask[4]),
            y3: parseInt(data.mask[5]),
            x4: parseInt(data.mask[6]),
            y4: parseInt(data.mask[7]),
          });
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  saveMask = () => {
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

    axios
      .post(`http://127.0.0.1:4000/cam01/mask`, mask, { timeout: 3000 })
      .then((response) => {
        Swal.fire({
          icon: "success",
          title: "Salvo.",
          text: "Máscara atualizada com sucesso!",
        });

      })
      .catch((error) => {
        Swal.fire({
          icon: "error",
          title: "Ops.",
          text: "Ocorreu algum erro ao atualizar máscara!",
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
