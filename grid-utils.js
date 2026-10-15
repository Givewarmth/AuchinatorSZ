const fs = require('fs');
const path = require('path');

const GRIDS_FILE = path.join(__dirname, 'data', 'grids.json');

let _grids = null;
function loadGrids() {
  if (_grids) return _grids;
  _grids = JSON.parse(fs.readFileSync(GRIDS_FILE, 'utf8'));
  return _grids;
}

function getGridForResolution(width, height, filename) {
  const grids = loadGrids();
  const key = width + 'x' + height;
  const block = grids[key];
  if (!block) throw new Error('No grid calibration for ' + key);

  const base = block.default || block;
  const grid = Object.assign({}, base);
  delete grid.overrides;

  if (filename && block.overrides && block.overrides[filename]) {
    const o = block.overrides[filename];
    for (const k of ['startX','startY','cellW','cellH','cols','rows']) {
      if (o[k] !== undefined) grid[k] = o[k];
    }
  }
  return grid;
}

module.exports = { loadGrids, getGridForResolution };