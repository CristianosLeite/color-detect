import styled from "styled-components"

export const PrincipalMostrarRgb = styled.div.attrs(props => ({
        title: props.title,
    })
)`
    display: flex;
    flex-direction: column;

    align-items: center;

    width: 310px;
    margin: 5px;
    //flex-wrap: wrap;
`

export const Header = styled.div`
    display: flex;
    flex-direction: column;
`;

export const Content = styled.div`
    display: flex;
    align-items: center;
`;

export const ContentCol01 = styled.div`
    display: flex;
    flex-direction: column;
`;

export const ContentCol01Linha02 = styled.div`
    display: flex;

    margin-left: 5px
`;


export const Title = styled.p`
    margin-bottom: 3px;
`;

export const InputHabilitaCor = styled.input`
    
`

export const MostradorDeCor = styled.div.attrs(props => ({
    corEscolhida: props.corEscolhida
}))`
    width: 40px;
    height: 40px;

    border-style: solid;
    border-radius: 5px;
    border-color: #000;
    border-width: 2px;

    background-color: rgb(${props => props.corEscolhida});

`

export const AjusteMinimo = styled.input`
`

export const Input = styled.input`
    width: 50px;
    
    margin: 5px;
`

