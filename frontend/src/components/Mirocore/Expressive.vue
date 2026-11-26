<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const expressiveCanvas = ref<HTMLCanvasElement | null>(null);

onMounted(() => {
  const canvas =  expressiveCanvas.value
  if (!canvas) return
  const dpr = window.devicePixelRatio || 1

  const width = canvas.clientWidth
  const height = width / 2

  canvas.width = Math.round(width * dpr)
  canvas.height = Math.round(height * dpr)

  canvas.style.height = `${height}px`
  canvas.style.width = `${width}px`

  const centerX = width / 2
  const centerY = height / 2
  const ctx =canvas.getContext('2d')
  if(!ctx) return

  // ctx.scale(dpr, dpr)
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  // drawFace(ctx, centerX, centerY, 1)
  MirocFaceAnimation(0, ctx, centerX, centerY, width, height)
})

function drawEyes(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  radius: number,
  distance: number,
  offset: number,
  element: "left" | "right",
  openness: number,
): void{
  ctx.beginPath()
  // 縦半径は？
  const radiusX = radius
  const radiusY = Math.max(1, radius * openness)
  // ellipse()を使って目を描画する
  if(element === "left"){
    ctx.ellipse(x - distance, y + offset, radiusX, radiusY, 0, 0, Math.PI * 2)
  }else{
    ctx.ellipse(x + distance, y + offset, radiusX, radiusY, 0, 0, Math.PI * 2)
  }
  ctx.fillStyle = '#232b2a'
  ctx.fill()
}

function drawMouth(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  offsetY: number,
  curve: number,
  width: number,
): void{
  ctx.beginPath()
  ctx.moveTo(x - width / 2, y + offsetY)
  ctx.quadraticCurveTo(x, y + offsetY + curve, x + width / 2, y + offsetY)
  ctx.strokeStyle = "#232b2a"
  ctx.lineWidth = 4
  ctx.lineCap = "round"
  ctx.stroke()
}

function drawFace(
  ctx: CanvasRenderingContext2D,
  centerX: number,
  centerY: number,
  openness: number,
): void{
  // 目のパラメータ
  const eyeRadius = 16
  const eyeDistance = 55
  const eyeOffset = -25

  // 口のパラメータ
  const mouthWidth = 40
  const mouthOffsetY = 20
  const mouthCurve = 18

  // 目の表示関数
  drawEyes(ctx, centerX, centerY, eyeRadius, eyeDistance, eyeOffset, "left", openness)
  drawEyes(ctx, centerX, centerY, eyeRadius, eyeDistance, eyeOffset, "right", openness)
  // 口の表示関数
  drawMouth(ctx, centerX, centerY, mouthOffsetY, mouthCurve, mouthWidth)
}

function calculateOpenness(
  timestamp: number
): number{
  const blinkInterval = 4000
  const blinkDuration = 200
  
  const phase = timestamp % blinkInterval
  const blinkStart = blinkInterval - blinkDuration

  if (phase < blinkStart){
    return 1
  }
  const progress = (phase - blinkStart) / blinkDuration

  return 1 - Math.sin(progress * Math.PI)
}

function MirocFaceAnimation(
  timestamp: number,
  ctx: CanvasRenderingContext2D,
  centerX: number,
  centerY: number,
  width: number,
  height: number,
): void{
  // 前の描写の削除
  ctx.clearRect(0, 0, width, height)
  // opennessの計算・更新
  const newOpenness = calculateOpenness(timestamp)
  // drawFace()を呼び出す
  drawFace(ctx, centerX, centerY, newOpenness)
  // 次のフレームの呼び出し
  requestAnimationFrame((timestamp) =>{
    MirocFaceAnimation(timestamp, ctx, centerX, centerY, width, height)
  })
}

</script>

<template>
    <div class="expressive">
        <canvas
          id="expressive-canvas"
          ref="expressiveCanvas"
        >
        </canvas>
    </div>
</template>

<style scoped>
.expressive {
  width: 100%;
}

#expressive-canvas {
  display: block;
  width: 100%;
  height: auto;
}
</style>