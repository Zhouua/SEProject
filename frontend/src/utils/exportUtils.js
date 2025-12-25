import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'
import { ElMessage } from 'element-plus'
import 'jspdf-autotable'

/**
 * 将ECharts图表导出为图片
 * @param {Object} chartInstance - ECharts实例
 * @returns {String} base64图片数据
 */
export const exportChartAsImage = async (chartInstance) => {
  if (!chartInstance) return null
  return chartInstance.getDataURL({
    type: 'png',
    pixelRatio: 2,
    backgroundColor: '#fff'
  })
}

/**
 * 导出多个图表到PDF
 * @param {Array} charts - 图表数组，每个元素包含 {title, instance, width, height}
 * @param {String} filename - 文件名
 */
export const exportChartsToPDF = async (charts, filename = 'report.pdf') => {
  try {
    ElMessage.info('正在生成PDF，请稍候...')
    
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4',
      compress: true
    })
    
    const pageWidth = pdf.internal.pageSize.getWidth()
    const pageHeight = pdf.internal.pageSize.getHeight()
    const margin = 15
    const contentWidth = pageWidth - 2 * margin
    
    // 创建一个隐藏的div来渲染中文文字
    const createTextImage = async (text, fontSize = 32, isBold = false) => {
      const tempDiv = document.createElement('div')
      tempDiv.style.position = 'fixed'
      tempDiv.style.left = '-9999px'
      tempDiv.style.top = '0'
      tempDiv.style.fontSize = `${fontSize}px`
      tempDiv.style.fontWeight = isBold ? 'bold' : 'normal'
      tempDiv.style.fontFamily = 'Arial, "Microsoft YaHei", "SimHei", sans-serif'
      tempDiv.style.color = '#000000'
      tempDiv.style.padding = '10px'
      tempDiv.style.backgroundColor = '#ffffff'
      tempDiv.textContent = text
      document.body.appendChild(tempDiv)
      
      const canvas = await html2canvas(tempDiv, {
        backgroundColor: '#ffffff',
        scale: 2
      })
      
      document.body.removeChild(tempDiv)
      return canvas.toDataURL('image/png')
    }
    
    // 添加标题页
    const title1 = await createTextImage('套利分析系统 - 数据概览报告', 48, true)
    pdf.addImage(title1, 'PNG', margin, 20, contentWidth, 15)
    
    const title2 = await createTextImage(`生成时间: ${new Date().toLocaleString('zh-CN')}`, 24)
    pdf.addImage(title2, 'PNG', margin, 40, contentWidth, 10)
    
    const title3 = await createTextImage('数据时间范围: 2025年9月1日 - 9月30日', 24)
    pdf.addImage(title3, 'PNG', margin, 55, contentWidth, 10)
    
    let yOffset = 80
    
    for (let i = 0; i < charts.length; i++) {
      const chart = charts[i]
      if (!chart.instance) continue
      
      // 添加新页
      pdf.addPage()
      yOffset = margin
      
      // 添加图表标题 - 使用html2canvas渲染中文
      const chartTitle = await createTextImage(chart.title || `Chart ${i + 1}`, 36, true)
      pdf.addImage(chartTitle, 'PNG', margin, yOffset, contentWidth, 12)
      yOffset += 18
      
      // 导出图表为图片
      const imgData = await exportChartAsImage(chart.instance)
      if (imgData) {
        // 计算图片尺寸（保持宽高比）
        const imgHeight = (contentWidth * chart.height) / chart.width
        const maxHeight = pageHeight - yOffset - margin
        
        if (imgHeight > maxHeight) {
          // 如果图片太高，缩小到合适尺寸
          const scale = maxHeight / imgHeight
          const scaledWidth = contentWidth * scale
          const scaledHeight = imgHeight * scale
          pdf.addImage(imgData, 'PNG', margin + (contentWidth - scaledWidth) / 2, yOffset, scaledWidth, scaledHeight)
        } else {
          pdf.addImage(imgData, 'PNG', margin, yOffset, contentWidth, imgHeight)
        }
      }
    }
    
    // 保存PDF
    pdf.save(filename)
    ElMessage.success('PDF导出成功！')
  } catch (error) {
    console.error('PDF导出失败:', error)
    ElMessage.error('PDF导出失败，请重试')
  }
}

/**
 * 导出数据为CSV
 * @param {Array} data - 数据数组
 * @param {Array} headers - 列头数组 [{key: 'field', label: 'Label'}]
 * @param {String} filename - 文件名
 */
export const exportToCSV = (data, headers, filename = 'data.csv') => {
  try {
    if (!data || data.length === 0) {
      ElMessage.warning('没有数据可以导出')
      return
    }
    
    // 添加BOM以支持Excel正确显示中文
    let csvContent = '\uFEFF'
    
    // 添加表头
    const headerRow = headers.map(h => h.label).join(',')
    csvContent += headerRow + '\n'
    
    // 添加数据行
    data.forEach(row => {
      const rowData = headers.map(h => {
        let value = row[h.key]
        
        // 处理特殊字符和格式
        if (value === null || value === undefined) {
          value = ''
        } else if (typeof value === 'string') {
          // 转义双引号并用双引号包裹含有逗号、换行或双引号的字段
          if (value.includes(',') || value.includes('\n') || value.includes('"')) {
            value = '"' + value.replace(/"/g, '""') + '"'
          }
        } else if (typeof value === 'number') {
          // 保留数字精度
          value = value.toString()
        }
        
        return value
      })
      csvContent += rowData.join(',') + '\n'
    })
    
    // 创建Blob并下载
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    
    link.setAttribute('href', url)
    link.setAttribute('download', filename)
    link.style.visibility = 'hidden'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    ElMessage.success('CSV导出成功！')
  } catch (error) {
    console.error('CSV导出失败:', error)
    ElMessage.error('CSV导出失败，请重试')
  }
}

/**
 * 导出Dashboard整体统计数据到CSV
 * @param {Object} stats - 统计数据
 * @param {String} filename - 文件名
 */
export const exportDashboardStats = (stats, filename = 'dashboard_stats.csv') => {
  const data = [
    { metric: '数据总记录数', value: stats.total_records || 0 },
    { metric: '套利机会总数', value: stats.arbitrage_opportunities?.count || 0 },
    { metric: '套利机会比例 (%)', value: stats.arbitrage_opportunities?.percentage || 0 },
    { metric: '最小套利收益 (USDT)', value: stats.arbitrage_opportunities?.min_profit || 0 },
    { metric: '最大套利收益 (USDT)', value: stats.arbitrage_opportunities?.max_profit || 0 },
    { metric: '平均套利收益 (USDT)', value: stats.arbitrage_opportunities?.avg_profit || 0 },
    { metric: '总潜在收益 (USDT)', value: stats.arbitrage_opportunities?.total_potential_profit || 0 },
    { metric: 'Binance 最低价格', value: stats.price_statistics?.binance?.min || 0 },
    { metric: 'Binance 最高价格', value: stats.price_statistics?.binance?.max || 0 },
    { metric: 'Binance 平均价格', value: stats.price_statistics?.binance?.avg || 0 },
    { metric: 'Uniswap 最低价格', value: stats.price_statistics?.uniswap?.min || 0 },
    { metric: 'Uniswap 最高价格', value: stats.price_statistics?.uniswap?.max || 0 },
    { metric: 'Uniswap 平均价格', value: stats.price_statistics?.uniswap?.avg || 0 }
  ]
  
  const headers = [
    { key: 'metric', label: '指标' },
    { key: 'value', label: '数值' }
  ]
  
  exportToCSV(data, headers, filename)
}
