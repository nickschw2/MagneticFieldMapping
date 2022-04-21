import nidaqmx
import numpy as np

class NI_DAQ():
    def __init__(self, dev_name, ai_channels, autoconnect=True):
        self.dev_name = dev_name
        self.ai_channels = ai_channels

        self.data = {name: np.array([]) for name in self.ai_channels} # analog input will be stored in this data array

        if autoconnect:
            self.set_up_tasks()
            print('NI DAQ has been successfully initialized')


    def set_up_tasks(self):
        '''
        Creates AI tasks
        '''
        self.h_task_ai = nidaqmx.Task('ai')

        # Add all channels
        for name, ai_chan in self.ai_channels.items():
            self.h_task_ai.ai_channels.add_ai_voltage_chan(f'{self.dev_name}/{ai_chan}')


    def read(self):
        points = self.h_task_ai.read()
        # put points into array if not already, ie if just reading from one channel
        if not isinstance(points, list):
            points = [points]

        values = {}
        for i, name in enumerate(self.ai_channels):
            self.data[name] = np.append(self.data[name], points[i])
            values[name] = points[i]

        return values

    def start_acquisition(self):
        self.h_task_ai.start()


    def stop_acquisition(self):
        self.h_task_ai.stop()

    # House-keeping methods follow
    def _task_created(self, task):
        '''
        Return True if a task has been created
        '''

        if isinstance(task, nidaqmx.task.Task):
            return True
        else:
            print('No tasks created: run the set_up_tasks method')
            return False

    def close(self):
        self.stop_acquisition()
        self.h_task_ai.close()
