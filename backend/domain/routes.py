from domain.studio_panels_api import router as studio_panels
from domain.floor_readings_api import router as floor_readings
from domain.optics_surveys_api import router as optics_surveys
from domain.practice_holds_api import router as practice_holds
from domain.dance_blocks_api import router as dance_blocks

routers = (studio_panels, floor_readings, optics_surveys, practice_holds, dance_blocks,)
