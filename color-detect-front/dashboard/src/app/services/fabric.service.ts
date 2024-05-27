import { Injectable } from '@angular/core';
import { fabric } from 'fabric';

@Injectable({
  providedIn: 'root'
})
export class FabricService {

  canvas: fabric.Canvas;

  constructor() {
    this.canvas = new fabric.Canvas('canvas', {
      width: 800,
      height: 800,
      backgroundColor: '#ffffff',
      selection: false
    });
  }

  addImage(url: string) {
    fabric.Image.fromURL(url, (img) => {
      this.canvas.add(img);
    });
  }

  addRect() {
    const rect = new fabric.Rect({
      left: 100,
      top: 100,
      fill: 'red',
      width: 20,
      height: 20
    });
    this.canvas.add(rect);
  }

  addCircle() {
    const circle = new fabric.Circle({
      left: 100,
      top: 100,
      fill: 'blue',
      radius: 20
    });
    this.canvas.add(circle);
  }

  addTriangle() {
    const triangle = new fabric.Triangle({
      left: 100,
      top: 100,
      fill: 'green',
      width: 20,
      height: 20
    });
    this.canvas.add(triangle);
  }

  addText(text: string) {
    const textObj = new fabric.Text(text, {
      left: 100,
      top: 100,
      fill: 'black',
      fontSize: 20
    });
    this.canvas.add(textObj);
  }

  clearCanvas() {
    this.canvas.clear();
  }

  saveCanvas() {
    const data = this.canvas.toDataURL();
    const a = document.createElement('a');
    a.href = data;
    a.download = 'canvas.png';
    a.click();
  }
}
