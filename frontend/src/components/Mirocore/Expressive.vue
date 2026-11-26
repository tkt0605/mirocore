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
  drawFace(ctx, centerX, centerY) 
})

function drawEyes(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  radius: number,
  distance: number,
  offset: number,
  element: "left" | "right",
): void{
  ctx.beginPath()
  if(element === "left"){
    ctx.arc(x - distance, y + offset, radius, 0, Math.PI * 2)
  }else{
    ctx.arc(x + distance, y + offset, radius, 0, Math.PI * 2)
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
  drawEyes(ctx, centerX, centerY, eyeRadius, eyeDistance, eyeOffset, "left")
  drawEyes(ctx, centerX, centerY, eyeRadius, eyeDistance, eyeOffset, "right")
  // 口の表示関数
  drawMouth(ctx, centerX, centerY, mouthOffsetY, mouthCurve, mouthWidth)
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