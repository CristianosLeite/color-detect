import { Component } from '@angular/core';
import { CanvasComponent } from '../../components/canvas/canvas.component';
import { HeaderComponent } from '../../components/header/header.component';
import { FooterComponent } from '../../components/footer/footer.component';
import { MaskConfigCardComponent } from '../../components/mask-config-card/mask-config-card.component';
import { ColorsCardComponent } from '../../components/colors-card/colors-card.component';
import { PlcConfigCardComponent } from '../../components/plc-config-card/plc-config-card.component';
import { ControllerConfigCardComponent } from '../../components/controller-config-card/controller-config-card.component';
import { ApiServiceService } from '../../services/api-service.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    HeaderComponent,
    CanvasComponent,
    FooterComponent,
    MaskConfigCardComponent,
    ColorsCardComponent,
    PlcConfigCardComponent,
    ControllerConfigCardComponent
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  ip: string = '';


}
