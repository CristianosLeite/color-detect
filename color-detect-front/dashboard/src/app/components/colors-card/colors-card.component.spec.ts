import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ColorsCardComponent } from './colors-card.component';

describe('ColorsCardComponent', () => {
  let component: ColorsCardComponent;
  let fixture: ComponentFixture<ColorsCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ColorsCardComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ColorsCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
