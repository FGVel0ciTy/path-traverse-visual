class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return " ".join([str(i) for i in self.queue])

    def __contains__(self, item):
        return item in self.queue

    def is_empty(self):
        return len(self.queue) == []

    def insert(self, item):
        self.queue.append(item)

    def remove(self):
        try:
            min_index = 0
            for index in range(len(self.queue)):
                if self.queue[index] < self.queue[min_index]:
                    min_index = index
            deleted_tile = self.queue[min_index]
            del self.queue[min_index]
            return deleted_tile
        except IndexError:
            print()
            exit()


class AStarQueue(PriorityQueue):
    def remove(self):
        try:
            min_f_index = 0
            for index in range(len(self.queue)):
                if self.queue[index].f < self.queue[min_f_index].f:
                    min_f_index = index
            deleted_tile = self.queue[min_f_index]
            del self.queue[min_f_index]
            return deleted_tile
        except IndexError:
            print()
            exit()


class DijkstraQueue(PriorityQueue):
    def remove(self):
        try:
            min_d_index = 0
            for index in range(len(self.queue)):
                if self.queue[index].d < self.queue[min_d_index].d:
                    min_d_index = index
            deleted_tile = self.queue[min_d_index]
            del self.queue[min_d_index]
            return deleted_tile
        except IndexError:
            print()
            exit()


class BreadthQueue(PriorityQueue):
    def remove(self):
        try:
            min_g_index = 0
            for index in range(len(self.queue)):
                if self.queue[index].g < self.queue[min_g_index].g:
                    min_g_index = index
            deleted_tile = self.queue[min_g_index]
            del self.queue[min_g_index]
            return deleted_tile
        except IndexError:
            print()
            exit()