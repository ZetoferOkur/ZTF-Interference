import numpy
import math
import matplotlib.pyplot as plt

SCREEN_SAMPLING_STEP = 0.01

class PointSource:
    def __init__(self, amplitude, wavelength, wave_speed, initial_phase, subsrc_coordinate):
        self.amplitude = amplitude
        self.phase = 0
        
        self.wavelength = wavelength
        self.wave_speed = wave_speed
        self.initial_phase = initial_phase
        self.subsrc_coordinate = subsrc_coordinate
        self.frequency = wave_speed/wavelength

    def phase_calc(self, curr_time_step, screen_distance, curr_screen_step):
        curr_coordinate = curr_screen_step * SCREEN_SAMPLING_STEP
        distance = math.sqrt(screen_distance**2 + (curr_coordinate - self.subsrc_coordinate)**2)
        self.phase = self.frequency * curr_time_step - (self.frequency / self.wave_speed) * distance + self.initial_phase


class Source:
    def __init__(self, src_coordinate, subsrcs_cnt,  subsrc_amplitude, subsrc_wavelength, subsrc_wave_speed, subsrc_initial_phase):
        self.amplitude = 0
        self.phase = 0
        
        self.subsrcs_cnt = subsrcs_cnt
        self.subsources_diversity = 1e-30
        
        self.subsrcs_coords = make_srcs_coordinates(subsrcs_cnt, self.subsources_diversity, src_coordinate)
        
        self.subsrcs_objs_list = []
        for i in range(0, subsrcs_cnt):
            self.subsrcs_objs_list.append(PointSource(subsrc_amplitude, subsrc_wavelength, subsrc_wave_speed, subsrc_initial_phase, subsrc_coordinate=self.subsrcs_coords[i]))


class Screen2D:
    def __init__(self, size, screen_distance):
        self.screen_distance = screen_distance
        self.screen_size = size
        self.buffer_size = int(size/SCREEN_SAMPLING_STEP)
        self.screen_steps = [x * SCREEN_SAMPLING_STEP for x in range(0, self.buffer_size)]  # Steps to meters
        self.screen_result_e_amplitude_buffer = numpy.zeros(self.buffer_size)
        self.screen_result_intensity_buffer = numpy.zeros(self.buffer_size)
        self.screen_result_e_phase_buffer = numpy.zeros(self.buffer_size)

    def two_waves_sum(self, wave_0_ampl, wave_1_ampl, wave_0_phase, wave_1_phase):
        ampl = math.sqrt(wave_0_ampl**2 + wave_1_ampl**2 + 2 * wave_0_ampl * wave_1_ampl * math.cos(wave_0_phase - wave_1_phase))
        phase = math.atan((wave_0_ampl * math.sin(wave_0_phase) + wave_1_ampl * math.sin(wave_1_phase)) / 
                          (wave_0_ampl * math.cos(wave_0_phase) + wave_1_ampl * math.cos(wave_1_phase)))
        return ampl, phase
    
    def sources_list_waves_sum(self, sources_list, sources_cnt):
        waves_ampl_buf = sources_list[0].amplitude
        waves_phase_buf = sources_list[0].phase
        
        for curr_source_index in range(1, sources_cnt):
            waves_ampl_buf, waves_phase_buf = self.two_waves_sum(waves_ampl_buf,
                                                                sources_list[curr_source_index].amplitude,
                                                                waves_phase_buf,
                                                                sources_list[curr_source_index].phase)
        return waves_ampl_buf, waves_phase_buf     

    def screen_calc(self, sources_list, curr_time_step, sources_cnt):
        for curr_screen_step in range(0, self.buffer_size):
            for curr_source in sources_list:
                for curr_subsource in curr_source.subsrcs_objs_list:
                    curr_subsource.phase_calc(curr_time_step, self.screen_distance, curr_screen_step)
                curr_source.amplitude, curr_source.phase = self.sources_list_waves_sum(curr_source.subsrcs_objs_list, curr_source.subsrcs_cnt)
            res_amplitude, res_phase = self.sources_list_waves_sum(sources_list, sources_cnt)
                
            self.screen_result_e_phase_buffer[curr_screen_step] = res_phase
            self.screen_result_e_amplitude_buffer[curr_screen_step] = res_amplitude
            self.screen_result_intensity_buffer[curr_screen_step] = res_amplitude ** 2
 
    # PLOTTING
    def plot_screen_buffers(self):
        fig, (ax, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex=True)
        # Interference picture
        extent = [self.screen_steps[0]-(self.screen_steps[1]-self.screen_steps[0])/2.,
                  self.screen_steps[-1]+(self.screen_steps[1]-self.screen_steps[0])/2., 0, 1]
        ax.imshow(self.screen_result_intensity_buffer[numpy.newaxis,:], cmap="plasma", aspect="auto", extent=extent)
        ax.set_yticks([])
        ax.set_xlim(extent[0], extent[1])

        # Intensity
        ax2.plot(self.screen_steps, self.screen_result_intensity_buffer, color="red")
        ax2.set_title("Intensity")

        # Amplitude
        ax3.plot(self.screen_steps, self.screen_result_e_amplitude_buffer, color="blue")
        ax3.set_title("Amplitude")
            
        # Phase
        ax4.plot(self.screen_steps, self.screen_result_e_phase_buffer, color="green")
        ax4.set_title("Phase")
        ax4.set_xlabel("Coordinate, m")

        plt.tight_layout()
        #plt.savefig("./osc.png", dpi=300)
        plt.show()
        input("Press 'Enter' key to exit...")
        
        
def make_srcs_coordinates(sources_cnt, sources_diversity, center_coordinate):
    sources_coordinates = []
    if (sources_cnt % 2) != 0 :
        sources_steps_cnt = int((sources_cnt - 1) / 2)
        sources_coordinates.append(center_coordinate)
    else:
        sources_diversity /= 2
        sources_steps_cnt = int(sources_cnt / 2)

    for j in range(1, sources_steps_cnt+1):
        if j == 1:
            sources_coordinates.append((center_coordinate) + sources_diversity)
            sources_coordinates.append((center_coordinate) - sources_diversity)
        else:
            sources_coordinates.append(sources_coordinates[-2] + sources_diversity * 2)
            sources_coordinates.append(sources_coordinates[-2] - sources_diversity * 2)
    return sources_coordinates

    
def main():
    curr_time_step = 200
    sources_diversity = 0.4 # m
    screen_distance = 4 # m
    screen_size = 50 # m

    sources_cnt = 2
    
    main_srcs_coords = make_srcs_coordinates(sources_cnt, sources_diversity, screen_size/2)

    # Make list of main sources
    sources_list = []
    for i in range(0, sources_cnt):
        sources_list.append(Source(src_coordinate=main_srcs_coords[i], subsrcs_cnt=1,  subsrc_amplitude=1, subsrc_wavelength=0.017, subsrc_wave_speed=340, subsrc_initial_phase=0))

    screen = Screen2D(screen_size, screen_distance)
    screen.screen_calc(sources_list, curr_time_step, sources_cnt)
    screen.plot_screen_buffers()
    
    
if __name__ == "__main__":
    main()
    